---
name: workspace-files
description: Work safely with files inside the OpenClaw workspace sandbox. Use for listing directories, reading text files, writing text files, and searching files by name inside ~/.openclaw/workspace only.
metadata: {"clawdbot":{"notes":["Sandbox limited to /home/cmart/.openclaw/workspace"]}}
---

# Workspace Files

Safe file operations limited to the OpenClaw workspace sandbox.

## Sandbox

All paths must stay inside:

/home/cmart/.openclaw/workspace

Do not use this skill for paths outside that sandbox.

## Quick Commands

- List a directory  
  `{baseDir}/scripts/workspace-files.sh list-dir "01_AGENTS"`

- Read a text file  
  `{baseDir}/scripts/workspace-files.sh read-file "TOOLS.md"`

- Write a text file  
  `{baseDir}/scripts/workspace-files.sh write-file "07_OUTPUTS/test.txt" "hola mundo"`

- Search files by name  
  `{baseDir}/scripts/workspace-files.sh search-files "SKILL.md"`

## Commands Reference

### list-dir

`{baseDir}/scripts/workspace-files.sh list-dir "<relative_path>"`

Examples:

- `{baseDir}/scripts/workspace-files.sh list-dir "."`
- `{baseDir}/scripts/workspace-files.sh list-dir "01_AGENTS"`

### read-file

`{baseDir}/scripts/workspace-files.sh read-file "<relative_path>"`

Examples:

- `{baseDir}/scripts/workspace-files.sh read-file "TOOLS.md"`
- `{baseDir}/scripts/workspace-files.sh read-file "01_AGENTS/_REGISTRY.md"`

### write-file

`{baseDir}/scripts/workspace-files.sh write-file "<relative_path>" "<content>"`

Example:

- `{baseDir}/scripts/workspace-files.sh write-file "07_OUTPUTS/demo.txt" "contenido de prueba"`

### search-files

`{baseDir}/scripts/workspace-files.sh search-files "<pattern>"`

Examples:

- `{baseDir}/scripts/workspace-files.sh search-files "SKILL.md"`
- `{baseDir}/scripts/workspace-files.sh search-files "compa"`

## Notes

- Only use relative paths inside the workspace sandbox.
- Intended for text files and directory inspection.
- Do not use for binary editing.
- Do not assume write access outside the sandbox.
