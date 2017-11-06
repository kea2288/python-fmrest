"""Record class for FileMaker record responses"""

class Record(object):
    """A FileMaker record representation.

    (with ideas from: https://github.com/kennethreitz/records)
    """
    __slots__ = ('_keys', '_values', '_in_portal', '_modifications')

    def __init__(self, keys, values, in_portal=False):
        """Initialize the Record class.

        Parameters
        ----------
        keys : list
            List of keys (fields) for this Record as returned by FileMaker Server
        values : list
            Values corresponding to keys
        in_portal : bool
            If true, this record instance describes a related record from a portal. This is a
            special case as portal records are treated differently by the Data API and don't get
            all standard keys (modId is missing).
        """

        self._keys = keys
        self._values = values
        self._in_portal = in_portal
        self._modifications = {}

        if len(self._keys) != len(self._values):
            raise ValueError("Length of keys does not match length of values.")

    def __repr__(self):
        return '<Record id={} modification_id={} is_dirty={}>'.format(
            self.record_id,
            self.modification_id,
            self.is_dirty
        )

    def __getitem__(self, key):
        """Returns value for given key. For dict lookups, like my_id = record['id']."""
        keys = self.keys()

        try:
            index = keys.index(key)
            return self.values()[index]
        except ValueError:
            raise KeyError(("No field named {}. Note that the Data API only returns fields "
                            "placed on your FileMaker layout.").format(key))

    def __getattr__(self, key):
        """Returns value for given key. For attribute lookups, like my_id = record.id.

        Calls __getitem__ for key access.
        """
        try:
            return self[key]
        except KeyError as ex:
            raise AttributeError(ex) from None

    def __setitem__(self, key, value):
        """Allows changing values of fields available in _keys.

        Modified keys land in _modifications and are later used to write values back to
        FileMaker.
        """
        if key not in self.__slots__:
            # objects in __slots__ are the only allowed attributes.
            # all others are handled here
            if key not in self.keys():
                raise KeyError(str(key) + " is not a valid field name.")
            elif key.startswith('portal_'):
                raise KeyError(
                    ("Portal data cannot be set through the record instance. "
                     "To edit portal data, build a dict and pass it to edit_records().")
                )
            elif value != self[key]:
                # store modified key and value for later re-use
                self._modifications[key] = value

                # also update the value in _values, so that values() returns expected data
                index = self.keys().index(key)
                self._values[index] = value
        else:
            # allow setting of attributes in __slots__
            super().__setattr__(key, value)

    def __setattr__(self, key, value):
        """See __setitem__. Returns AttributeError if trying to set a value for a field/attribute
        not existing in the record instance.
        """
        try:
            return self.__setitem__(key, value)
        except KeyError as ex:
            raise AttributeError(ex) from None

    def modifications(self):
        """Returns a dict of changed keys in the form of {key : new_value}.

        Used for writing back record changes via Server.edit(record).
        """
        return self._modifications

    @property
    def is_dirty(self):
        """Returns True if key values have been modified."""
        return len(self._modifications) > 0

    @property
    def record_id(self):
        """Returns the internal record id.

        This is exposed as a method to reliably return the record id, even if the API might change
        the field name in the future.
        """
        return int(self.recordId)

    @property
    def modification_id(self):
        """Returns the internal modification id.

        This is exposed as a method to reliably return the modification id, even if the API might
        change the field name in the future.
        """
        return None if self._in_portal else int(self.modId)

    def keys(self):
        """Returns all keys of this record."""
        return self._keys

    def values(self):
        """Returns all values of this record."""
        return self._values
