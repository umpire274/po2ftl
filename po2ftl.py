import polib
import argparse

# Define the version of the script
__version__ = "1.0.0"


# Function to convert PO files to FTL format
def po_to_ftl(po_file, ftl_file):
    po = polib.pofile(po_file)  # Load the PO file
    with open(ftl_file, 'w') as ftl:
        for entry in po:
            # Remove dots in the key names and use the correct format for variables
            key = entry.msgid.replace('.', '_')  # Replace dots with underscores
            key = key.replace('//', 'doubleslash')  # Replace '_//' with '_doubleslash'
            key = key.replace('-', 'minus')
            key = key.replace('+', 'plus')

            # Handle variables in the msgstr
            value = entry.msgstr.replace('{name}', '{ $name }')

            # Handle pluralization
            if entry.msgid_plural:  # Check if plural form exists
                # Safely get singular and plural values from msgstr_plural list
                singular = entry.msgstr_plural[0] if len(entry.msgstr_plural) > 0 else ""
                plural = entry.msgstr_plural[1] if len(entry.msgstr_plural) > 1 else ""

                # Write Fluent pluralization syntax
                ftl.write(f"{key} = {{ $unreadEmails ->\n")
                ftl.write(f"    [one] {singular}\n")
                ftl.write(f"   *[other] {plural}\n")
                ftl.write(f"}}\n")
            else:
                # If no pluralization, write just the key with its translation
                ftl.write(f"{key} = {value}\n")


# Function to configure the command-line interface
def main():
    parser = argparse.ArgumentParser(description='Convert a PO file to FTL format.')
    parser.add_argument('-in', '--input', required=True, help='Path to the input .po file')
    parser.add_argument('-out', '--output', required=True, help='Path to the output .ftl file')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}',
                        help="Show the version of the script")

    # Parse the arguments
    args = parser.parse_args()

    # Call the conversion function
    po_to_ftl(args.input, args.output)
    print(f"Conversion completed: {args.input} → {args.output}")


if __name__ == '__main__':
    main()
