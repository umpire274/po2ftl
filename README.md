# PO to FTL Converter aka *po2ftl*

This utility converts **PO** files (gettext translation files) into **FTL** files (Fluent Translation files). The **FTL** format is used for localization in modern applications, and it provides a more powerful and flexible way to handle translations compared to traditional gettext systems.

## Features

- Convert `.po` files to `.ftl` format.
- Supports handling of pluralization.
- Handles variables in translation strings (e.g., `{name}` becomes `{ $name }`).
- Replaces special characters in keys (e.g., `//` becomes `doubleslash`).

## Requirements

- Python 3.x
- `polib` (for handling `.po` files)

## Installation

To install the necessary dependencies, run the following:

```bash
pip install polib
```
## Usage

The converter can be run from the command line. You can specify the input `.po` file and the output `.ftl` file using the `-in` and `-out` parameters.

## Command-Line Usage

```bash
python po2ftl.py -in <input.po> -out <output.ftl>
```

## Example

If you have a file messages.po that you want to convert to messages.ftl, you would run:

```bash
python po2ftl.py -in messages.po -out messages.ftl
```

## Version

To display the version of the script, use the --version flag:

```bash
python po2ftl.py --version
```

This will output:

```bash
po2ftl.py 1.0.0
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you'd like to contribute to this project, feel free to fork it, create a pull request, or open an issue for discussion. All contributions are welcome!

## Acknowledgements

This project uses the [polib](https://github.com/python-poetry/polib) library to read and write .po files.
