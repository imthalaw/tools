import os
import sys

def strip_prefix_from_filenames(directory, prefix):
    """
    Recursively walks through a directory and renames files by stripping a given prefix.

    Args:
        directory (str): The path to the top-level directory to start from.
        prefix (str): The prefix string to remove from the beginning of filenames.
    """
    # Check if the provided directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory not found at '{os.path.abspath(directory)}'")
        return

    print(f"Starting scan in directory: {os.path.abspath(directory)}")
    print(f"Looking for files starting with prefix: '{prefix}'\n")

    # A counter for the number of files renamed
    renamed_files_count = 0

    # os.walk generates the file names in a directory tree.
    for root, dirs, files in os.walk(directory):
        print(f"Scanning folder: {root}")
        for filename in files:
            # Check if the filename starts with the specified prefix
            if filename.startswith(prefix):
                # Construct the full old and new file paths
                old_filepath = os.path.join(root, filename)
                # Slice the string to remove the prefix
                new_filename = filename[len(prefix):]
                new_filepath = os.path.join(root, new_filename)

                try:
                    # Rename the file
                    os.rename(old_filepath, new_filepath)
                    print(f"  - Renamed: '{filename}' -> '{new_filename}'")
                    renamed_files_count += 1
                except OSError as e:
                    # Handle potential errors like permission denied
                    print(f"  - Error renaming '{filename}': {e}")
        print("-" * 20)

    print(f"\nScan complete. Renamed {renamed_files_count} file(s).")

if __name__ == "__main__":
    # The script name is sys.argv[0], so we expect 3 arguments total.
    if len(sys.argv) != 3:
        print("\nUsage: python your_script_name.py <target_directory> \"<prefix_to_strip>\"")
        print("Example: python your_script_name.py ./docs \"MPFC \"")
        print("\nNote: Remember to put the prefix in quotes if it contains spaces.")
        sys.exit(1) # Exit the script if arguments are incorrect

    # The first argument (sys.argv[1]) is the directory.
    target_directory = sys.argv[1]
    
    # The second argument (sys.argv[2]) is the prefix string.
    prefix_to_strip = sys.argv[2]

    # Run the main function with the provided arguments
    strip_prefix_from_filenames(target_directory, prefix_to_strip)
