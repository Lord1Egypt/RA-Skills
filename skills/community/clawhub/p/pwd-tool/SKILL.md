---
name: pwd-tool
description: Print the full path of the current working directory. Use for identifying your location in the filesystem.
---
# PWD - Print Working Directory

Display the absolute path of the current working directory. Essential for navigation awareness and script path management.

## Usage
```bash
pwd-tool [options]
```

## Options

- `-P`: Show physical path (resolve symlinks)
- `-L`: Show logical path (with symlinks, default)

## Examples

```bash
pwd-tool
pwd-tool -P
```