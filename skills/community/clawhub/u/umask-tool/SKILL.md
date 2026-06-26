---
name: umask-tool
description: Set or display file creation permission mask. Use for controlling default file permissions on new files and directories.
---
# Umask - Permission Mask Utility

Set the file mode creation mask which determines default permissions for newly created files and directories. The mask subtracts permissions from the default 666 (files) or 777 (directories).

## Usage
```bash
umask-tool [options] [mask]
```

## Examples

```bash
# Show current mask
umask-tool

# Set restrictive mask (files: 600, dirs: 700)
umask-tool 077

# Set permissive mask (files: 644, dirs: 755)
umask-tool 022
```