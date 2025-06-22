# mkmediafold.py

import os
import shutil # For working with files and folders
import sys # For cli arguments

def build_folders_mv_files(target_folder):
  """
  Scans a target folder and for each file, creates a new folder named after
  the file (without extension) and move the file into it.
  """
  print(f"Scanning target folder: {target_folder}\n")

  try:
    all_items = os.listdir(target_folder)
  except FileNotFoundError:
    print(f"Error: The folder '{target_folder}' does not exist.")
    return

  for filename in all_items:
    original_file_path = os.path.join(target_folder, filename)

    if os.path.isfile(original_file_path):
      print(f"Processing file: {filename}")
      folder_name, file_extension = os.path.splitext(filename)
      new_folder_path = os.path.join(target_folder, folder_name)

      if not os.path.exists(new_folder_path):
        try:
          os.makedirs(new_folder_path)
          print(f"  -> Created folder: {new_folder_path}")
        except OSError as e:
          print (f" -> Error creating folder {new_folder_path}: {e}")
          continue
      else:
        print(f"  -> Folder '{folder_name}' already exists.")

      try:
        shutil.move(original_file_path, new_folder_path)
        print(f"  -> Moved '{filename}' into '{new_folder_path}'\n")
      except Exception as e:
        print(f"  -> Error moving file {filename}: {e}\n")
    else:
      print(f"Skipping directory: {filename}\n")
  print("Program complete!")

# ---------- setting target and instructions -------
if __name__ == "__main__":
  # Check if arg was given
  if len(sys.argv) < 2:
    # If not arg is given we print instructions that someone may need.
    print("Usage: \n python mkmediafold.py /home/you/targetfolder")
    print("You can also drag and drop the folder onto the terminal after the script name.")
    print("If it still isn't working try running as administrator or with sudo.")
    sys.exit(1) # Exit stage left

  # First arg is target
  target_path = sys.argv[1]

  # Starting engines
  build_folders_mv_files(target_path)
  
