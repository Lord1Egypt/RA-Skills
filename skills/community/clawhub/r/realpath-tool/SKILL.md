---
name: realpath-tool
description: Resolve relative paths and symbolic links to absolute canonical paths. Use for getting the full, unambiguous file path.
---
# Realpath - Absolute Path Resolver

Convert relative paths and symlinks to absolute canonical paths. Useful for scripts that need the full path of files, directories, or symlinked resources.

## Usage
```bash
realpath-tool [options] <path...>
```

## Options

- `-s`: Don't expand symlinks (show logical path)
- `-m`: Path doesn't need to exist
- `--relative-to=DIR`: Show path relative to DIR

## Examples

```bash
realpath-tool ./relative/path
realpath-tool -s symlink_path
realpath-tool --relative-to=/home file.txt
```