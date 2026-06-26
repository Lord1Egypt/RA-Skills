# Session Cleanup — Reference Guide

This reference is loaded by the session-cleanup Skill when the agent needs
exact commands for uninstalling packages or removing files across different
operating systems and package managers.

---

## 1. File & Directory Removal

### Windows (PowerShell)

```powershell
# Move single file to Recycle Bin (safe)
$shell = New-Object -ComObject Shell.Application
$item = $shell.NameSpace(0).ParseName('C:\path\to\file.txt')
$item.InvokeVerb('delete')

# Remove a directory (ONLY use on confirmed temp paths)
Remove-Item -Path "C:\Users\user\AppData\Local\Temp\mysession" -Recurse -Force
```

### macOS (Bash)

```bash
# Move to Trash
osascript -e 'tell app "Finder" to delete POSIX file "/path/to/file"'

# Direct remove (temp only)
rm -rf /tmp/mysession/
```

### Linux (Bash)

```bash
# Use gio trash (preferred)
gio trash /tmp/mysession/

# Alternative
trash-put /tmp/mysession/

# Direct remove (temp only)
rm -rf /tmp/mysession/
```

---

## 2. Python Package Uninstall

```bash
# Uninstall a single package
pip uninstall -y requests

# Uninstall multiple packages
pip uninstall -y requests httpx aiohttp

# List installed packages to confirm removal
pip list | grep requests

# Uninstall all packages listed in a requirements file
pip uninstall -y -r requirements.txt
```

---

## 3. npm Package Uninstall

```bash
# Global package
npm uninstall -g lodash

# Local project package
npm uninstall lodash

# List installed global packages
npm list -g --depth=0
```

---

## 4. System Software Uninstall

### Windows — winget

```powershell
winget uninstall --id <PackageID>
winget uninstall --name "Package Name"

# Example
winget uninstall --id Python.Python.3.11
```

### Windows — Chocolatey

```powershell
choco uninstall <package-name> -y

# Example
choco uninstall nodejs -y
```

### macOS — Homebrew

```bash
brew uninstall <formula>

# Example
brew uninstall node

# Remove orphan dependencies
brew autoremove
```

### Linux — apt

```bash
sudo apt remove <package>
sudo apt purge <package>     # also removes config files
sudo apt autoremove          # remove orphaned dependencies

# Example
sudo apt remove nodejs
```

### Linux — snap

```bash
sudo snap remove <package>

# Example
sudo snap remove code
```

---

## 5. WorkBuddy Skill Removal

Skills are stored as directories. To remove a skill:

```powershell
# Windows PowerShell
Remove-Item -Path "$env:USERPROFILE\.workbuddy\skills\skill-name" -Recurse -Force

# macOS/Linux
rm -rf ~/.workbuddy/skills/skill-name/
```

To list installed user skills:

```powershell
# Windows
Get-ChildItem "$env:USERPROFILE\.workbuddy\skills\"

# macOS/Linux
ls ~/.workbuddy/skills/
```

---

## 6. Cleanup Manifest Format

The `cleanup.py` script accepts a JSON manifest. Example:

```json
{
  "temp_files": [
    "C:/Users/<user>/AppData/Local/Temp/demo_script.py",
    "C:/Users/<user>/AppData/Local/Temp/test_output.txt"
  ],
  "pip_packages": [
    "requests",
    "httpx"
  ],
  "npm_packages": [
    "live-server"
  ],
  "skills": [
    "C:/Users/<user>/.workbuddy/skills/my-test-skill"
  ],
  "other": []
}
```

Run cleanup from the skill directory:

```bash
python scripts/cleanup.py --manifest /path/to/manifest.json
python scripts/cleanup.py --manifest /path/to/manifest.json --dry-run
```

Run cleanup directly from session-track.json (recommended — inherits workspace awareness):

```bash
python scripts/cleanup.py --track-file /path/to/session-track.json
python scripts/cleanup.py --track-file /path/to/session-track.json --dry-run
```

**Note:** When using `--track-file`, the script reads the `workspace` field from the JSON and uses it for safety checks. This allows workspace subdirectories like `generated-images/` to be correctly identified as safe to delete.

---

## 7. Safe Temp Path Reference

The following directories are considered safe for auto-deletion without user confirmation:

| OS | Safe Temp Paths |
|---|---|
| Windows | `%TEMP%`, `%TMP%`, `%USERPROFILE%\AppData\Local\Temp` |
| macOS | `/tmp`, `/var/folders/...` (per-session) |
| Linux | `/tmp`, `/var/tmp` |
| Any OS | Workspace `generated-images/` folder, explicitly named `*_temp`, `*_scratch`, `*_demo` files |

**Never auto-delete** paths under:
`Desktop`, `Downloads`, `Documents`, `~` (home root), `C:\`, `/`, workspace source directories.
