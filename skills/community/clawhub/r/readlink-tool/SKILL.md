---
name: readlink-tool
description: Display the target of a symbolic link. Use for resolving symlinks to find the actual file or directory they point to.
---
# Readlink - Symbolic Link Resolver

Show the target path that a symbolic link points to. Essential for understanding symlink chains and finding actual file locations.

## Usage
```bash
readlink-tool [options] <link>
```

## Options

- `-f`: Canonicalize by following every symlink in the path
- `-e`: Canonicalize but require all components to exist
- `-n`: Suppress trailing newline

## Examples

```bash
readlink-tool /usr/bin/python
readlink-tool -f symlink_to_file
readlink-tool -e symlink.txt
```