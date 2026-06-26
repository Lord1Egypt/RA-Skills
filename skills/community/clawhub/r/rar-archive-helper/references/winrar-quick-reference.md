# RAR / WinRAR Quick Reference

## Detect the executable

### Windows
```bat
where rar
where winrar
set PATH=C:\Program Files\WinRAR;%PATH%
```

### PowerShell
```powershell
$env:Path = "C:\Program Files\WinRAR;" + $env:Path
```

### Linux
```bash
command -v rar
which rar
export PATH=/path/to/rar-directory:$PATH
```

## Common install locations

### Windows
- `C:\Program Files\WinRAR`
- `C:\Program Files (x86)\WinRAR`
- `%LOCALAPPDATA%\Programs\WinRAR`

### Linux
- `/usr/bin`
- `/usr/local/bin`
- `/opt`
- `/usr/local/rar`
- `~/bin`

## Official download links

### Windows
`https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-720.exe`

### Linux
`https://www.win-rar.com/fileadmin/winrar-versions/rarlinux-x64-720.tar.gz`

## Core commands

### Extract with full paths
```bash
rar x archive.rar /path/to/output/
```

### Extract without full paths
```bash
rar e archive.rar /path/to/output/
```

### Extract with password
```bash
rar x -pPASSWORD archive.rar /path/to/output/
```

### Windows password examples
```bat
winrar x -p123456 secure.zip
winrar x -pabc123 C:\files\archive.rar D:\output\
winrar x -p"p@ss!word" data.rar
winrar x -ibck -p123456 archive.rar D:\output\
```

### Create archive
```bash
rar a archive.rar /path/to/files/*
```

### Create password archive
```bash
rar a -p archive.rar /path/to/files/*
```

### Create split volumes
```bash
rar a -v100m archive.part.rar /path/to/files/*
```

### Extract first volume of multipart set
```bash
rar x archive.part1.rar /path/to/output/
```

## Helpful switches
- `x`: extract with full paths
- `e`: extract without stored paths
- `a`: add files to archive
- `-p`: provide password
- `-ibck`: background mode on Windows
- `-o+`: overwrite existing files
- `-y`: answer yes to prompts

## Encoding tip for Chinese paths on Windows
```bat
chcp 65001
```

## Troubleshooting checklist
- check `PATH` first;
- try `rar` and `winrar` on Windows;
- quote passwords with special characters;
- quote paths with spaces;
- start multipart extraction from the first volume;
- use `-o+ -y` if overwrite prompts block automation;
- see `references/common-errors.md` for detailed fixes.
