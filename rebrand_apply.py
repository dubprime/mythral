import os
import re
import shutil

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

def replace_in_file(filepath):
    global total_replacements
    rel_path = os.path.relpath(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"[WARN] Could not read {rel_path}: {e}")
        return 0
    original_content = content
    for pat, repl in REPLACEMENTS:
        content = re.sub(pat, repl, content)
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        num_replacements = sum(len(re.findall(pat, original_content)) for pat, _ in REPLACEMENTS)
        file_hits[rel_path] = num_replacements
        total_replacements += num_replacements
        print(f"[REPLACED] {rel_path}: {num_replacements} replacements")
        return num_replacements
    return 0

def rename_path(path, is_dir=False):
    base = os.path.basename(path)
    new_base = base
    for pat, repl in REPLACEMENTS:
        new_base = re.sub(pat, repl, new_base)
    if new_base != base:
        new_path = os.path.join(os.path.dirname(path), new_base)
        if not os.path.exists(new_path):
            shutil.move(path, new_path)
            rel_old = os.path.relpath(path)
            rel_new = os.path.relpath(new_path)
            if is_dir:
                renamed_dirs.append((rel_old, rel_new))
                print(f"[RENAMED DIR] {rel_old} -> {rel_new}")
            else:
                renamed_files.append((rel_old, rel_new))
                print(f"[RENAMED FILE] {rel_old} -> {rel_new}")
            return new_path
    return path

def main():
    print("--- APPLYING REBRANDING: Mythral → Mythral, DubPrime → DubPrime ---\n")
    # Walk the tree bottom-up to avoid renaming parent dirs before children
    for root, dirs, files in os.walk('.', topdown=False):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        # Rename files
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SKIP_EXTENSIONS:
                continue
            filepath = os.path.join(root, f)
            if is_binary_file(filepath):
                continue
            replace_in_file(filepath)
            new_filepath = rename_path(filepath)
        # Rename directories
        for d in dirs:
            dirpath = os.path.join(root, d)
            rename_path(dirpath, is_dir=True)
    print("\n--- SUMMARY ---")
    print(f"Files with replacements: {len(file_hits)}")
    print(f"Total replacements made: {total_replacements}")
    print(f"Files renamed: {len(renamed_files)}")
    print(f"Directories renamed: {len(renamed_dirs)}")
    if file_hits:
        print("\nFiles with replacements:")
        for f, n in file_hits.items():
            print(f"  {f} ({n} replacements)")
    if renamed_files:
        print("\nFiles renamed:")
        for old, new in renamed_files:
            print(f"  {old} -> {new}")
    if renamed_dirs:
        print("\nDirectories renamed:")
        for old, new in renamed_dirs:
            print(f"  {old} -> {new}")
    print("\nRebranding complete.")

if __name__ == '__main__':
    main() 