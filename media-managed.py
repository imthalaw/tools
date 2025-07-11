import os
import re # for working with regex and finding those patterns.
import sys
import argparse 
import shutil

def move_files_to_individual_folder(target_folder):
    """
    For each file in the target folder (non-recursive), create a folder named after the file (minus extension),
    and move the file into its corresponding folder.
    """
    print(f"Scanning target folder for file-to-folder organization: {targer_folder}\n")

    try:
        all_items = os.lisdir(target_folder)
    except FileNotFoundError:
        print(f"Error: The folder '{target_folder}' does not exist.")
        return

for filename in all_items:
    original_file_path = os.path.join(target_folder, filename)

    # Only process files (skip directories)
    if os.path.isfile(original_file_path):
        print(f"Processing file: {filename}")
        folder_name, file_extension = os.path.splitext(filename)
        new_folder_fath = os.path.join(target_folder, folder_name)

        if not os.path.exists(new_folder_path):
            try:
                os.makedirs(new_folder_path)
                print(f"  -> Created folder: {new_folder_path}")
            except OSError as e:
                print(f"  -> Error creating folder {new_folder_path}: {e}")
                continue
        else:
            print(f"  -> Folder '{folder_name}' already exists.")

        try:
            shutil.move(original_file_path, new_folder_path)
            print(f"  -> Moved '{filename}' into '{new_folder_path}'\n")
        except Exception as e:
            print(f"  -> Error movie file {filename}: {e}\n")
    else:
        Print(f"Skipping directory: {filename}\n")
print("Move-to-folder operation complete!")


def process_filename(filename, prefix=None, postfix=None, remove_str=None, perform_clean=False):
    """
    Modifies a filename by stripping text or cleaning characters.
    Order of operations: 1. Prefix, 2. Postfix, 3. Remove, 4. Clean.
    """
    name_part, extension = os.path.splitext(filename)
    new_name_part = name_part

    # 1. Strip the prefix (from the beginning)
    if prefix and new_name_part.startswith(prefix):
        new_name_part = new_name_part[len(prefix):]

    # 2. Strip the postfix (from the end)
    if postfix and new_name_part.endswith(postfix):
        new_name_part = new_name_part[:-len(postfix)]

    # 3. Remove all occurrences of a specific substring
    if remove_str:
        new_name_part = new_name_part.replace(remove_str, "")

    # 4. Perform a general cleanup of common unwanted characters
    if perform_clean:
        # Define characters to replace with a space using a regex pattern
        # This will replace one or more occurrences of these characters with a single space
        # Added '\' before '-' to escape it in the regex character set
        new_name_part = re.sub(r'[_.\-]+', ' ', new_name_part)

        # Define strings to remove completely using a regex pattern
        # The re.IGNORECASE flag makes the matching case-insensitive
        # Sort by length descending to ensure longer patterns are matched first
        chars_to_remove = [
            'web-dl', 'blueray', 'dd5.1', 'cmrg',
            '[tgx]', 'hevc', 'webrip', 'hdr', 'av1', 'opus', 
            '5.1', 'h265', 'x265', 'x264', 'h264'
        ]
        
        # Create a regex pattern that matches any of the strings to remove, case-insensitively
        # We need to escape characters like '[' and ']' that have special meaning in regex
        # Use a non-capturing group (?:...) for better performance
        pattern_to_remove = r'|'.join([re.escape(s) for s in sorted(chars_to_remove, key=len, reverse=True)])
        new_name_part = re.sub(pattern_to_remove, '', new_name_part, flags=re.IGNORECASE)
        
        # Remove any remaining curly braces specifically
        new_name_part = new_name_part.replace('{', '').replace('}', '')

        # Consolidate multiple spaces into a single space and remove leading/trailing whitespace
        new_name_part = " ".join(new_name_part.split()).strip() # Added .strip() at the end

    # Return the new filename only if a change was made
    if new_name_part != name_part:
        return new_name_part.strip() + extension # Ensure stripping happens before adding extension
    else:
        return filename

def rename_files_in_directory(directory, prefix=None, postfix=None, remove_str=None, perform_clean=False):
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
    if perform_clean:
        print(f" - Will perform general filename cleaning.")
    print("-" * 20)

    renamed_files_count = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Pass the clean flag to the processing function
            new_filename = process_filename(filename, prefix, postfix, remove_str, perform_clean)

            if new_filename != filename:
                old_filepath = os.path.join(root, filename)
                new_filepath = os.path.join(root, new_filename)
                
                # Prevent overwriting an existing file
                if os.path.exists(new_filepath):
                    print(f"  - Skipped (conflict): Renaming '{filename}' to '{new_filename}' would overwrite an existing file.")
                    continue
                
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
        epilog="Example: python media-managed.py ./my_files --prefix \"DRAFT-\" --clean"
    )
    
    parser.add_argument("directory", help="The target directory to scan.")
    parser.add_argument("-p", "--prefix", help="The prefix to strip from the start of filenames.")
    parser.add_argument("-s", "--postfix", help="The postfix to strip from the end of filenames (before extension).")
    parser.add_argument("-r", "--remove", dest="remove_str", help="A string to remove from anywhere within filenames.")
    parser.add_argument("-m", "--mkfolders", action="store_ture", help="For each file, create a folder (named after the file, minus extension) and move the file into it after renaming/cleaning.")
    parser.add_argument("-c", "--clean", action="store_true", help="Perform a general cleanup (replaces '_', '.', '-' with spaces and removes common unwanted strings).")
    
    args = parser.parse_args()

    # Make sure at least one action is selected
    if not any([args.prefix, args.postfix, args.remove_str, args.clean, args.mkfolders]):
        print("Error: You must specify at least one operation: --prefix, --postfix, --remove, --clean, --mkfolders.")
        parser.print_help()
        sys.exit(1)

    # Pass the new 'clean' argument to the function
    rename_files_in_directory(args.directory, args.prefix, args.postfix, args.remove_str, args.clean args.mkfolders)
    
    # Optionally, move each file into ies own folder after renaming/cleaning
    if args.mkfolders:
        move_files_to_individual_folders(args.directory)
