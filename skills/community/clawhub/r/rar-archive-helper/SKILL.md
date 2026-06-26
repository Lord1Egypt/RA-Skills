---
name: rar-command-helper
description: cross-platform rar and winrar command-line archive handling for windows and linux. use when chatgpt needs to compress or extract archives with rar or winrar, detect whether rar tools are available, repair path issues, download official installers when missing, handle password-protected archives, process multipart archives, and troubleshoot common command-line extraction or compression errors in automation workflows.
---

# Overview
Use this skill for reliable archive compression and extraction with `rar` or `winrar` on Windows and Linux.

Core responsibilities:
- Detect whether `rar` or `winrar` is callable
- Search common install locations if the command is missing
- Add the executable location to `PATH` when possible
- Fall back to the official download links if the binary is not installed
- Run compression or extraction commands
- Handle passwords, special characters, multipart archives, overwrite prompts, and common automation failures
- Use a single evidence-based retry when the failure cause is clear

## Required execution order
Always follow this sequence:

`Goal -> Detect -> Fix PATH -> Run -> Verify -> Result`

Do not skip detection. Do not jump straight to archive commands unless the executable is already known to work.

## Platform detection
First determine whether the environment is Windows or Linux, then use the matching commands and path conventions.

## Detect availability

### Windows
Run:
```bash
where rar
where winrar
```

### Linux
Run:
```bash
which rar
```

If at least one valid executable is found, prefer that executable and continue.

## Search common install locations when the command is missing

### Windows common locations
- `C:\Program Files\WinRAR\`
- `C:\Program Files (x86)\WinRAR\`

Check for:
- `rar.exe`
- `winrar.exe`

### Linux common locations
- `/usr/bin/rar`
- `/usr/local/bin/rar`
- `/opt/rar/`

If found, either call the binary by absolute path or add its directory to `PATH`.

## Add to PATH

### Windows temporary PATH update
```bash
set PATH=C:\Program Files\WinRAR;%PATH%
```

### Windows persistent PATH update
```bash
setx PATH "%PATH%;C:\Program Files\WinRAR"
```

### Linux temporary PATH update
```bash
export PATH=$PATH:/usr/local/bin
```

If modifying `PATH` is not allowed or does not take effect in the current shell, use the absolute executable path.

## Official download fallback
If the executable is not found in common locations, use the official download link that matches the platform.

### Windows
`https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-720.exe`

### Linux
`https://www.win-rar.com/fileadmin/winrar-versions/rarlinux-x64-720.tar.gz`

Only suggest or perform download after detection and common-path checks fail.

## Extraction commands

### Basic extraction with full paths
```bash
rar x archive.rar
```

### Extract to a target directory
```bash
rar x archive.rar /output/path/
```

### Extract without preserving paths
```bash
rar e archive.rar
```

## Password-protected extraction

### Basic password form
```bash
rar x -p123456 archive.rar
```

### Password with output directory
```bash
rar x -p123456 archive.rar /output/path/
```

### Password with special characters
Wrap the password in quotes when it contains shell-significant characters.
```bash
rar x -p"p@ss!word" archive.rar
```

On Windows, equivalent `winrar` examples are valid:
```bash
winrar x -p123456 secure.zip
winrar x -pabc123 C:\files\archive.rar D:\output\
winrar x -p"p@ss!word" data.rar
```

## Silent or unattended extraction
Use background or unattended flags for automation:
```bash
rar x -ibck -p123456 archive.rar /output/path/
```

Use overwrite and yes-to-all flags when prompts would block automation:
```bash
rar x -o+ -y archive.rar
```

## Compression commands

### Create archive
```bash
rar a archive.rar file1 file2
```

### Create encrypted archive
```bash
rar a -p123456 archive.rar file1
```

### Create split archive
```bash
rar a -v100m archive.rar largefile.iso
```

## Encoding and path handling

### Windows UTF-8 console for Chinese path issues
If Chinese paths or filenames display as garbled text, run:
```bash
chcp 65001
```

### Paths with spaces
Always quote paths containing spaces:
```bash
"C:\path with space\file.rar"
```

### Absolute path fallback on Windows
```bash
"C:\Program Files\WinRAR\winrar.exe" x archive.rar
```

## Multipart archive handling
Always start extraction from the first volume, typically:
- `part1.rar`
- `archive.part1.rar`

Do not start from later volumes.

## Verification
After running the archive command, verify:
- Expected output files exist
- The target directory exists
- The command output does not indicate password, CRC, path, or permission failures

If verification fails, inspect the error and decide whether the single retry rule applies.

## Single retry rule
Retry at most once, and only when the failure cause is concrete and fixable.

Allowed retry cases:
- Fixed a PATH issue
- Corrected a password
- Added quotes around a special-character password
- Added quotes around a path with spaces
- Switched to the first part of a multipart archive
- Added overwrite flags to avoid blocking prompts
- Fixed encoding with `chcp 65001`
- Switched to absolute executable path

Do not retry when:
- The archive appears corrupted
- The error remains unknown
- The environment blocks execution for unrelated reasons
- The same command already failed after the relevant fix

## Standard execution template
Use this exact reporting structure in responses:

```text
[Goal]
<what needs to be done>

[Detect]
<what command was checked and what was found>

[Fix PATH]
<how PATH or executable resolution was handled>

[Run]
<the command executed>

[Verify]
<what was checked>

[Result]
Status: SUCCESS or FAILED
Command: <final command>
Output: <key output>
Notes: <important notes, or none>
```

## Common errors and fixes

### Command not found
Cause:
- `rar` or `winrar` is not in `PATH`

Fix:
- Search common install directories
- Add the directory to `PATH`
- Use absolute path
- Download from the official link if not installed

### Wrong executable name
Cause:
- Windows may expose `winrar`
- Linux usually uses `rar`

Fix:
- Try both names on Windows
- Prefer `rar` on Linux

### Incorrect password
Symptoms:
- Extraction fails
- Prompt repeats
- Output indicates wrong password or file header failure

Fix:
- Re-enter the correct password
- Quote passwords with special characters:
```bash
-p"p@ss!word"
```

### Path contains spaces
Fix:
- Quote every path argument that contains spaces

### Chinese path garbling
Fix:
- Run `chcp 65001` before the archive command on Windows terminals where encoding is the issue

### Permission denied
Fix:
- Change the output directory
- Elevate privileges when appropriate
- Use a writable working directory

### Multipart extraction failure
Cause:
- Extraction started from a later volume

Fix:
- Start from the first volume only

### Overwrite prompt blocks automation
Fix:
```bash
-o+ -y
```

### PATH cannot be modified
Fix:
- Use the full absolute path to `rar.exe` or `winrar.exe`

## Behavioral constraints
- Prefer CLI operations over GUI instructions
- Be concise and operational
- Do not invent installation locations; only use detected or common ones
- Use the official download URLs provided above
- Show the final command clearly
- State uncertainty when a failure cause is not confirmed
