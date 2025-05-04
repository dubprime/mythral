import os
import sys
import re
from pathlib import Path

# Terms to search and their replacements
REPLACEMENTS = [
    (r'Mythral', 'Mythral'),
    (r'mythral', 'mythral'),
    (r'DubPrime', 'DubPrime'),
    (r'dubprime', 'dubprime'),
]

# File extensions to skip (binaries, images, etc.)
SKIP_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.exe', '.bin', '.pyc', '.zip', '.tar', '.gz', '.pdf', '.mp3', '.mp4', '.mov', '.ogg', '.wav', '.webm', '.svg', '.DS_Store', '.inv', '.buildinfo'
}

# Directories to skip
SKIP_DIRS = {'.git', '__pycache__'}

# For summary
file_hits = {}
total_replacements = 0
renamed_files = []
renamed_dirs = []


def is_binary_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return True
    except Exception:
        return True
    return False

def check_file_content(filepath):
    global total_replacements
    rel_path = os.path.relpath(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[WARN] Could not read {rel_path}: {e}")
        return
    hits = []
    for i, line in enumerate(lines, 1):
        for pat, repl in REPLACEMENTS:
            for match in re.finditer(pat, line):
                hits.append((i, pat, match.group(0), line.strip()))
    if hits:
        file_hits[rel_path] = hits
        total_replacements += len(hits)
        print(f"\n[CONTENT] {rel_path}")
        for (lineno, pat, found, snippet) in hits:
            print(f"  Line {lineno}: '{found}' (pattern: {pat}) -> '{snippet}'")

def check_name(path, is_dir=False):
    rel_path = os.path.relpath(path)
    for pat, repl in REPLACEMENTS:
        if re.search(pat, os.path.basename(path)):
            if is_dir:
                renamed_dirs.append(rel_path)
                print(f"[DIRNAME] Would rename directory: {rel_path}")
            else:
                renamed_files.append(rel_path)
                print(f"[FILENAME] Would rename file: {rel_path}")
            break

def main():
    print("--- DRY RUN: Rebranding Mythral → Mythral, DubPrime → DubPrime ---\n")
    for root, dirs, files in os.walk('.'):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        # Check directory names
        for d in dirs:
            check_name(os.path.join(root, d), is_dir=True)
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SKIP_EXTENSIONS:
                continue
            filepath = os.path.join(root, f)
            if is_binary_file(filepath):
                continue
            check_name(filepath)
            check_file_content(filepath)
    print("\n--- SUMMARY ---")
    print(f"Files with content matches: {len(file_hits)}")
    print(f"Total replacements found: {total_replacements}")
    print(f"Files needing renaming: {len(renamed_files)}")
    print(f"Directories needing renaming: {len(renamed_dirs)}")
    if file_hits:
        print("\nFiles with matches:")
        for f in file_hits:
            print(f"  {f} ({len(file_hits[f])} matches)")
    if renamed_files:
        print("\nFiles to rename:")
        for f in renamed_files:
            print(f"  {f}")
    if renamed_dirs:
        print("\nDirectories to rename:")
        for d in renamed_dirs:
            print(f"  {d}")
    print("\nNo files were modified. This was a dry run.")

if __name__ == '__main__':
    main() 