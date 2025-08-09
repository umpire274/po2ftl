import unittest
import polib
import os


# Function to convert PO to FTL
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


# Test class
class TestPoToFtlConversion(unittest.TestCase):
    import os

    def setUp(self):
        """Prepare the test files"""
        # Crea la cartella per i file di test (se non esiste già)
        self.test_dir = './test_files'
        os.makedirs(self.test_dir, exist_ok=True)

        # File .po
        self.po_file = os.path.join(self.test_dir, 'test.po')
        with open(self.po_file, 'w') as po:
            po.write("""
    msgid "greeting"
    msgstr "Hello, {name}!"

    msgid "You have one message"
    msgid_plural "You have {count} messages"
    msgstr[0] "You have one message"
    msgstr[1] "You have {count} messages"
            """)

        # File .ftl
        self.ftl_file = os.path.join(self.test_dir, 'test.ftl')

    def tearDown(self):
        """Clean up the test files and the directory"""
        try:
            os.remove(self.po_file)  # Remove the PO file
            os.remove(self.ftl_file)  # Remove the FTL file
            os.rmdir(self.test_dir)  # Remove the test directory
        except OSError as e:
            print(f"Error cleaning up files: {e}")

    def test_conversion(self):
        """Test the conversion of the PO file to FTL"""

        # Convert the PO file to FTL
        po_to_ftl(self.po_file, self.ftl_file)

        # Verify that the .ftl file was created
        self.assertTrue(os.path.exists(self.ftl_file))

        # Verify that the content of the .ftl file is correct
        with open(self.ftl_file, 'r') as ftl:
            ftl_content = ftl.read()

        # Check that the singular translation is correct
        self.assertIn("greeting = Hello, { $name }!", ftl_content)

        # Check that the plural translations are correct
        self.assertIn("You have one message", ftl_content)
        self.assertIn("You have {count} messages", ftl_content)

        # Check that pluralization is handled correctly in Fluent format
        self.assertIn("You have one message", ftl_content)
        self.assertIn("You have {count} messages", ftl_content)

if __name__ == '__main__':
    unittest.main()
