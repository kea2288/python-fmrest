# python-fmrest

python-fmrest is a wrapper around the FileMaker Data API.

No need to worry about manually requesting access tokens, setting the right http headers, parsing responses, ...

Quick example:

```python
>>> fms = fmrest.Server('https://your-server.com',
                        user='admin',
                        password='admin',
                        database='Contacts',
                        layout='Contacts')
>>> fms.login()
>>> record = fms.get_record(1)
>>> record.name
John Doe
```

## Supported Features

All API paths can be served:

- auth
- record
- find
- global

## It's still early! Feel free to contribute!

The module is still in development and likely has some issues and missing parts ⚠️ (also see [TODO](#to-do) section below) If you would like to contribute, you can help with the code, try it out and report 🐞🐞, propose new features, write tests, add examples and documentation.

There's always room for improvement!

---

**Note that there might still be some breaking changes ahead. Also note, that the FileMaker Data API is still in trial phase.**

Questions/problems? Open a [new issue](https://github.com/davidhamann/python-fmrest/issues). You can also contact me directly at dh@davidhamann.de.

## Install

You need Python 3 and FileMaker Server/Cloud 16 (below there is no Data API 😎)

For now, install it like this:

```
python setup.py install
```

## Local development / running tests

Make sure to have requirements-dev.txt installed:

```
pip install -r requirements-dev.txt
```

Running `pytest` will run all tests. To run specific tests, specify the path:

```
pytest tests/unit
```

For running `tests/integration` you will need to have a real FileMaker Server running.

## Usage Examples

Examples can be found in the [examples](https://github.com/davidhamann/python-fmrest/tree/master/examples) directory.

## TO DO
<a id="to-do"></a>

Some bits and pieces that are essential, and some that would be nice to have, are not implemented yet.

Examples of what I can think of:

- Record instances are not fully fledged yet. There is no Record instance support for editing portal data (currently, you must go via edit_records and pass a dict if you want to edit portal data), no support for creation (must use `Server.create_record`), deletion (must use `Server.delete_record`), etc. I began implementing field level changes, so you can already do something like this: `record.name = 'changed name'` and then `Server.edit(record)`. This will track what you changed and only write back the changes.
- Handling of reserved field names (currently, `record_id`, `modification_id`, `is_dirty` clash with used properties and you will not be able to read your own fields with the same name)
- Some more usage examples on how to create, edit, delete, set globals, etc. Tell me where you have issues by opening an [issue](https://github.com/davidhamann/python-fmrest/issues).
- Remote container fetching would be nice
- cli support would also be great
