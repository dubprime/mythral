#!/bin/bash

# Exit on error
set -e

SRC_DIR="$(pwd)"
PARENT_DIR="$(dirname "$SRC_DIR")"
NEW_DIR="$PARENT_DIR/mythral"

# 1. Copy the directory
if [ -d "$NEW_DIR" ]; then
    echo "[INFO] Directory 'mythral' already exists. Skipping copy."
else
    echo "[INFO] Copying project to 'mythral'..."
    cp -r "$SRC_DIR" "$NEW_DIR"
fi

cd "$NEW_DIR"

# 2. Initialize a new git repo if not already present
if [ -d ".git" ]; then
    echo "[INFO] Git repo already initialized in 'mythral'."
else
    echo "[INFO] Initializing new git repository..."
    git init
    git add .
    git commit -m "Initial commit: pre-rebranding"
fi

# 3. Print instructions for next steps
cat <<EOM

[INFO] Project cloned to 'mythral' and git repo initialized.

Next steps:
1. cd "$NEW_DIR"
2. Run your rebranding script (e.g., python3 rebrand_apply.py)
3. git add .
4. git commit -m "Apply Mythral and DubPrime rebranding"
5. (Optional) git remote add origin <your-new-repo-url>
6. (Optional) git push -u origin main

EOM 