---
name: wsl-path-converter
description: Convert Windows paths to WSL paths for file operations in WSL environment
author: OpenClaw Assistant
version: 1.0.0
---

# WSL path conversion skills
This skill is used to convert Windows paths to WSL paths, enabling correct access to Windows files in the WSL environment.

## Function Description
In the WSL environment, the disk partitions of Windows are mounted under the `/mnt/` directory, for example:
- `C:\` → `/mnt/c/`
- `E:\` → `/mnt/e/`
This skill can automatically recognize the Windows path format and convert it into a path accessible by WSL.

## Usage
The skill will automatically handle path conversion. When you provide a path in Windows format, it will be automatically converted to WSL format.

## Example
When you mentioned a similar path:
- `E:\projects\chess_game.png` → automatically converted to `/mnt/e/projects/chess_game.png`
- `C:\Users\Documents\file.txt` → automatically converted to `/mnt/c/Users/Documents/file.txt`
- `D:\data\images\photo.jpg` → automatically converted to `/mnt/d/data/images/photo.jpg`

## Conversion Rules
1. Recognize Windows paths in the format of `X:\`
2. Convert it to the `/mnt/x/` format
3. Convert the Windows path separator `\` to the Unix path separator `/`
4. Keep the rest of the path unchanged

## Application Scenario
- Read files from Windows disks
- Access project files in Windows
- Manipulate images or other resources in Windows
- Handle Windows paths in the WSL environment