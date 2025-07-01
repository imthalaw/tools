import os
import sys
import argparse

def process_filename(filename, prefix=None, postfix=None, remove_str=None):
    """
    Modifies a filename by stripping text.
    Order of operations: 1. Prefix, 2. Postfix, 3. Remove (all occurrences).
    """
    name_part, extension = os.path.splitext(filename)
    new_name_part = name_part

    # 1. Strip the prefix (from the beginning)
    if prefix and new_name_part.startswith(prefix):
        new_name_part = new_name_part[len(prefix):]

    # 2. Strip the postfix (from the end)
    if postfix and new_name_part.endswith(postfix):
        new_name_part = new_name_part[:-len(postfix)]

    # 3. Remove all occurrences of a substring (from anywhere)
    if remove_str:
        new_name_part = new_name_part.replace(remove_str, "")

    # Return the new filename only if a change was made
    if new_name_part != name_part:
        return new_name_part + extension
    else:
        return filename

def rename_files_in_directory(directory, prefix=None, postfix=None, remove_str=None):
    """ Recursively renames files based on the provided operations. """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found at '{os.path.abspath(directory)}'")
        return

    print(f"Starting scan in directory: {os.path.abspath(directory)}")
    if prefix:
        print(f" - Will strip prefix: '{prefix}'")
    if postfix:
        print(f" - Will strip postfix: '{postfix}'")
    if remove_str:
        print(f" - Will remove all instances of: '{remove_str}'")
    print("-" * 20)

    renamed_files_count = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            new_filename = process_filename(filename, prefix, postfix, remove_str)

            if new_filename != filename:
                old_filepath = os.path.join(root, filename)
                new_filepath = os.path.join(root, new_filename)
                try:
                    os.rename(old_filepath, new_filepath)
                    print(f"  - Renamed: '{filename}' -> '{new_filename}'")
                    renamed_files_count += 1
                except OSError as e:
                    print(f"  - Error renaming '{filename}': {e}")
    
    print("-" * 20)
    print(f"\nScan complete. Renamed {renamed_files_count} file(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recursively strip prefixes, postfixes, or any substring from filenames.",
        epilog="Example: python your_script.py ./files --remove \"-copy\""
    )
    
    parser.add_argument("directory", help="The target directory to scan.")
    parser.add_argument("-p", "--prefix", help="The prefix to strip from the start of filenames.")
    parser.add_argument("-s", "--postfix", help="The postfix to strip from the end of filenames (before extension).")
    parser.add_argument("-r", "--remove", dest="remove_str", help="A string to remove from anywhere within filenames.")
    
    args = parser.parse_args()

    if not any([args.prefix, args.postfix, args.remove_str]):
        print("Error: You must specify at least one operation: --prefix, --postfix, or --remove.")
        parser.print_help()
        sys.exit(1)

    rename_files_in_directory(args.directory, args.prefix, args.postfix, args.remove_str)