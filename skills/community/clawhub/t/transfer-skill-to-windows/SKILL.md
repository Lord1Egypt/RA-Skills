---
name: transfer-skill-to-windows
description: Adapt an existing agent skill so it works cleanly on Windows when the input is either a skill folder path or a zip file.
---

# Transfer Skill To Windows

Use this skill when the user wants to make an existing skill work on Windows, especially when the original skill assumes Unix shells, Unix paths, or Linux/macOS tooling.

This skill accepts either:

- A path to a skill folder
- A path to a zip file that contains a skill folder

The goal is to produce a Windows-compatible version of the skill with the smallest practical set of changes, while preserving the original workflow and intent.

Default output policy:

- Preserve the original input
- Prefer a sibling output folder with a clear suffix such as `_windows_ready`
- If the source input is a zip file, also produce a rebuilt Windows-ready zip that matches the converted folder

## What This Skill Produces

This skill helps you:

- Inspect the incoming skill package or folder
- Detect whether a partially converted Windows copy already exists
- Identify Windows-incompatible assumptions
- Rewrite instructions, commands, and examples for Windows
- Repair machine-specific path mistakes introduced by earlier conversions
- Preserve cross-platform behavior when practical
- Return an updated skill folder ready to use on Windows
- Rebuild and verify the zip artifact when the source was a zip file

## When To Use This Skill

Use this skill when the user asks for any of the following:

- Transfer a skill to Windows
- Make a skill support Windows
- Convert a skill that uses bash or Unix paths
- Patch a skill distributed as a folder or zip so it works on Windows

Do not use this skill for general application migration. This skill is specifically for agent skills and their supporting files.

## Inputs To Gather

Before making changes, confirm or infer the following:

1. The input type:
   - Skill folder path
   - Zip file path
2. The desired output behavior:
   - In-place update
   - Create a separate Windows-ready copy
3. Whether the user wants:
   - Windows-only support
   - Cross-platform support with Windows compatibility

Also check whether there is already a derived output nearby, for example:

- `<skill>_windows`
- `<skill>_windows_ready`
- an extracted folder that matches the zip name
- an existing Windows-ready zip

If the user does not specify output behavior, default to creating a separate Windows-ready copy so the source remains untouched.

## Workflow

### 1. Load The Skill Contents

If the input is a folder:

- Inspect the directory structure
- Locate `SKILL.md` and any helper scripts, templates, or config files
- Check whether a Windows-oriented sibling copy already exists and may need to be updated rather than recreated

If the input is a zip file:

- Extract it to a working directory
- Inspect the extracted contents
- Identify the actual skill root that contains `SKILL.md`
- Check for an existing extracted or converted copy before creating a new one

If the extracted archive does not contain a `SKILL.md`, stop and tell the user the package does not look like a valid skill.

If multiple candidate outputs already exist, prefer this order:

1. A clearly named Windows-ready copy that already contains Windows files such as `.ps1`
2. A partially converted copy that still needs fixes
3. A fresh extraction from the original input

### 2. Inventory Windows Risks

Inspect `SKILL.md` and any referenced files for these common issues:

- Commands written only for `bash`, `sh`, or `zsh`
- Use of `&&`, `export`, `chmod`, `rm`, `cp`, `mv`, `cat`, `grep`, `sed`, `awk`, `find`, `xargs`, `tar`, `unzip`, or `which`
- Unix-style absolute paths such as `/tmp/...` or `/usr/local/...`
- Machine-specific absolute paths embedded in docs or code, such as `/home/...` or `C:\Users\...`
- Path examples that assume `/` separators in shell commands
- Shebang-based scripts such as `#!/bin/bash`
- Scripts that depend on executable permission bits
- References to tools commonly missing on Windows
- Instructions that assume case-sensitive filesystems
- Symlink-heavy workflows without Windows fallback guidance
- Test or helper code that imports via hardcoded absolute paths
- Documentation that points to the wrong output folder after conversion

Also inspect supporting files such as:

- `.ps1`, `.bat`, `.cmd`, `.sh`
- `_meta.json`
- `package.json`
- `pyproject.toml`
- `requirements.txt`
- README or usage examples
- Template files referenced by the skill

### 3. Decide The Conversion Strategy

Prefer this order of solutions:

1. Make instructions tool-based rather than shell-specific when possible
2. Replace Unix-only shell examples with PowerShell equivalents
3. Fix runtime-affecting path assumptions before polishing documentation
4. Keep cross-platform examples if they are already valid on Windows
5. Add Windows notes only where a direct rewrite would reduce clarity

If a command can be expressed in a VS Code tool workflow, prefer that over raw shell instructions.

### 4. Rewrite For Windows

Apply the smallest change set that makes the skill usable on Windows.

Typical rewrites include:

- Replace bash command examples with PowerShell examples
- Replace `export NAME=value` with `$env:NAME = 'value'`
- Replace `rm -rf path` with `Remove-Item -Recurse -Force path`
- Replace `cp src dst` with `Copy-Item src dst`
- Replace `mv src dst` with `Move-Item src dst`
- Replace `cat file` with `Get-Content file`
- Replace `grep pattern file` with `Select-String -Path file -Pattern pattern`
- Replace `which tool` with `Get-Command tool`
- Replace `chmod +x script.sh` by removing the permission requirement or by providing a `.ps1` alternative
- Replace archive extraction examples with `Expand-Archive`
- Replace Unix temp-directory assumptions with Windows-safe paths or tool-managed temp locations
- Replace hardcoded import paths with paths derived from the current file location
- Replace machine-specific documentation paths with relative paths when the skill is expected to be moved between machines

Also normalize instructional language:

- Use Windows path examples when showing local filesystem paths
- Prefer relative paths in examples when the skill folder is portable
- Avoid telling users to invoke `bash -lc` unless that is a hard requirement
- Prefer PowerShell 5.1 compatible commands unless the skill clearly requires PowerShell 7+

Do not treat these as mandatory problems by themselves:

- Python shebang lines in `.py` files, if the files otherwise run on Windows
- Preserved `.sh` scripts kept for Linux or macOS compatibility, if Windows alternatives are added and documented

### 5. Update Supporting Files

If the skill includes helper scripts:

- Convert `.sh` scripts into `.ps1` equivalents when needed
- Update references inside `SKILL.md` to the new script names
- Preserve original scripts if the goal is cross-platform support
- If a Windows-native script already exists, validate its behavior and references before rewriting it

If the skill contains examples or templates with shell snippets:

- Rewrite those snippets for Windows
- Keep the original semantics intact

If the skill references zipped input or extracted folders:

- Ensure the instructions explicitly say how to handle both on Windows

If the source was a zip file:

- Ensure the converted folder structure is stable and self-contained
- Rebuild a Windows-ready zip from the converted folder
- Verify the rebuilt archive contents before finishing

### 6. Validate The Result

Before finishing, verify:

- `SKILL.md` still describes the original task accurately
- Every command shown is runnable on Windows or clearly marked otherwise
- Any referenced files actually exist after conversion
- Paths and examples are internally consistent
- The skill does not rely on Unix-only permission or shell behavior without explanation
- The documentation does not reference the wrong sibling output directory
- Any runtime imports or script references do not depend on a machine-specific absolute path
- If the input was a zip file, the rebuilt zip contains the expected converted root and files

### 7. Report The Outcome

Summarize:

- What Windows incompatibilities were found
- Which files were changed
- Whether the result is Windows-only or cross-platform
- Whether an existing partial conversion was reused or corrected
- Whether a new Windows-ready zip was rebuilt and verified
- Any remaining limitations, such as required third-party tools

## Decision Rules

- If the skill is documentation-only, focus on rewriting instructions and examples
- If the skill contains scripts, convert the scripts or provide Windows-native alternatives
- If the skill depends on a Unix-only tool with no practical Windows equivalent, call that out explicitly and propose the least disruptive fallback
- If the user provides a zip file, do not assume the archive root is the skill root; inspect it first
- If the user provides a folder path, do not duplicate large files unless the user asked for a separate output
- If a Windows-ready output already exists, inspect it before creating another copy
- If a converted copy already contains a plausible Windows script, prefer validating and fixing it over regenerating everything
- If code and docs disagree, fix the runtime-critical issue first and then align the docs

## Completion Criteria

The task is complete when:

- A valid `SKILL.md` exists in the converted skill
- Windows users can follow the instructions without relying on bash-only behavior
- Any required helper files are updated or replaced
- Any hardcoded machine-specific path assumptions have been removed or justified
- If the source was a zip, a rebuilt Windows-ready zip exists and its contents were verified
- The user receives a concise summary of the migration and any remaining caveats

## Example Prompts

- Convert this skill folder to work on Windows: `C:\skills\my-skill`
- Adapt this zipped skill for Windows support and keep it cross-platform: `C:\downloads\my-skill.zip`
- Audit this skill for Unix-only assumptions and produce a Windows-ready copy

## Notes For The Agent

- Prefer precise edits over broad rewrites
- Preserve the author's intent and workflow
- Do not remove useful cross-platform guidance unless it conflicts with Windows usability
- Treat pre-existing `_windows` or `_windows_ready` folders as evidence to inspect, not clutter to ignore
- Absolute paths inside docs and tests are high-priority smells because they often survive superficial conversions
- A conversion is not finished until the packaged artifact matches the edited folder when the input was a zip file
- If the skill is ambiguous, ask one focused question after producing the first draft of the conversion plan