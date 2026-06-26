# qshell Installation Guide

## Windows

1. Go to [qshell GitHub Releases](https://github.com/qiniu/qshell/releases)
2. Download `qshell-windows-amd64.zip` (for 64-bit systems, which is most modern PCs)
3. Extract to a directory (e.g., `C:\Tools\qshell\`)
4. The extracted file may be named `qshell-windows-amd64.exe` — rename it to `qshell.exe` for convenience
5. Add that directory to the system PATH environment variable:
   - Press `Win + S`, search for "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find `Path`, double-click to edit
   - Click "New", enter the directory path (e.g., `C:\Tools\qshell`)
   - Click "OK" to save
6. Reopen terminal, verify with `qshell --version`

**Windows-specific notes:**
- Do NOT double-click `qshell.exe` directly — it is a CLI tool that must run inside cmd or PowerShell. Double-clicking causes it to flash and close immediately.
- Use backslashes `\` in file paths (e.g., `D:\photos\image.jpg`), or forward slashes also work in most cases.
- Use double quotes `"` for strings in commands and config files, not single quotes.
- When editing config files (e.g., for qupload2), use a plain text editor and save as UTF-8 encoding to avoid garbled Chinese characters.

## macOS

**Option A (recommended):**
```bash
brew install qshell
```

**Option B:** Download from [GitHub Releases](https://github.com/qiniu/qshell/releases):
- Intel Mac: `qshell-darwin-amd64.zip`
- Apple Silicon: `qshell-darwin-arm64.zip`

Extract and move to PATH:
```bash
unzip qshell-darwin-*.zip
chmod +x qshell
sudo mv qshell /usr/local/bin/
```

## Linux

1. Download from [GitHub Releases](https://github.com/qiniu/qshell/releases) (e.g., `qshell-linux-amd64.tar.gz`)
2. Extract and install:
   ```bash
   tar -xzf qshell-linux-amd64.tar.gz
   chmod +x qshell
   sudo mv qshell /usr/local/bin/
   ```
3. Verify: `qshell --version`
