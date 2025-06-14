#!/bin/sh

TARGET_DIR="."

# Option to specify a different target directory
# Example: ./extract_files.sh /tmp/diff_target_directory
if [ -n "$1" ]; then
TARGET_DIR="$1"
fi

echo "Extracting Files from all subdirectories..."

find . -mindepth 2 -type f -exec mv {} "$TARGET_DIR" \;

echo "Files extracted. Now cleaning up!"

find . -mindepth 1 -type d -exec rmdir {} \; 2>/dev/null

echo "Cleanup complete, end program.
