---
name: tree-tool
description: Display directory structure as an indented tree. Use for visualizing folder hierarchies and project structure.
---
# Tree - Directory Listing Tree

Recursively list directory contents in a tree-like format. Shows files and folders with indentation to visualize the complete directory structure.

## Usage
```bash
tree-tool [options] [path]
```

## Options

- `-L N`: Limit depth to N levels
- `-d`: Show directories only
- `-a`: Show hidden files
- `-h`: Print file sizes
- `-I pattern`: Exclude files matching pattern

## Examples

```bash
tree-tool
tree-tool -L 2 /home/user
tree-tool -d -L 1
```