# Tool Installation Guide

Detailed installation procedures for `BBDown` (Bilibili) and `yt-dlp` (YouTube) on Windows. Reference this when SKILL.md's Step 1 detects a missing tool.

> **Path convention**: examples below use `<TOOLS_DIR>` as a placeholder for the tool storage directory. The agent invoking this skill chooses the concrete path (see "Directory Conventions" in SKILL.md). **Recommended default: `~/bin/videolink-to-article/`** (`%USERPROFILE%\bin\videolink-to-article\` on Windows). This naming pattern (`~/bin/<skill-name>/`) is meant to be reused across other skills, keeping each skill's tools isolated from each other and from the rest of the user's system.
>
> **Every install procedure ends with adding `<TOOLS_DIR>` to PATH** — see § "Persisting tools to PATH" below. Without this final step, every new agent session re-runs the install probe and the user has to re-confirm/re-install. With it, tools are directly callable as `BBDown.exe` / `yt-dlp.exe` in any new shell.

---

## Installing BBDown (for Bilibili)

BBDown is a single-file `.exe`, no installer required.

### Method A — winget (easiest, often blocked by network)

```powershell
winget install --id nilaoda.BBDown -e --accept-source-agreements --accept-package-agreements
```

If winget fails silently with exit code 1, fall through to Method B.

### Method B — Direct download from GitHub release

Resolve the latest version via API:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$r = Invoke-RestMethod -Uri "https://api.github.com/repos/nilaoda/BBDown/releases/latest" `
    -UseBasicParsing -Headers @{ "User-Agent"="ps" }
$asset = $r.assets | Where-Object { $_.name -match "win.*x64.*\.zip$" } | Select-Object -First 1
$asset.browser_download_url
```

Direct download is **frequently blocked in Mainland China** because `api.github.com` is reachable but `objects.githubusercontent.com` (the release CDN) is not. Symptoms: `curl: (35) schannel: failed to receive handshake, SSL/TLS connection failed`.

### Method C — GitHub mirror fallback (recommended for China network)

Wrap the GitHub URL with `https://gh-proxy.com/`:

```powershell
$tools = "<TOOLS_DIR>"   # <TOOLS_DIR> is chosen by the invoking agent (recommended: ~/bin/videolink-to-article/)
New-Item -ItemType Directory -Force -Path $tools | Out-Null
$mirrors = @(
    "https://gh-proxy.com/https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_win-x64.zip",
    "https://ghproxy.net/https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_win-x64.zip",
    "https://mirror.ghproxy.com/https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_win-x64.zip"
)
foreach ($u in $mirrors) {
    curl.exe -L --max-time 60 -o "$tools\BBDown.zip" $u
    if ((Test-Path "$tools\BBDown.zip") -and ((Get-Item "$tools\BBDown.zip").Length -gt 100000)) { break }
    Remove-Item "$tools\BBDown.zip" -ErrorAction SilentlyContinue
}
Expand-Archive -Path "$tools\BBDown.zip" -DestinationPath $tools -Force
Remove-Item "$tools\BBDown.zip"
```

Replace the version string with the latest tag from the API call in Method B if 1.6.3 is outdated.

### ffmpeg workaround for BBDown

BBDown performs a startup check for `ffmpeg` and refuses to run without it, even in subtitle-only mode (where ffmpeg is never actually invoked).

If `ffmpeg` is not installed system-wide, pass any existing executable as a placeholder:

```powershell
BBDown.exe "<URL>" --sub-only --skip-ai false `
  --ffmpeg-path "<TOOLS_DIR>\yt-dlp.exe"   # any existing exe works; yt-dlp.exe is convenient if already installed in the same TOOLS_DIR
```

The path just needs to point to a real file; BBDown does not validate it as ffmpeg.

### BBDown login (only if needed)

For most public videos, AI subtitles work without login. If a specific video requires authentication, see `auth.md` § Method 1 (BBDown QR-code login).

---

## Authentication

For login flows (BBDown QR code, yt-dlp cookies-from-browser, manual cookies.txt export), see **`auth.md`**. That file covers when authentication is needed, the three login methods, and known pitfalls (App-Bound Encryption, cookie DB locks).

---

## Installing yt-dlp (for YouTube)

`yt-dlp` is a self-contained Python script bundled into a single Windows `.exe` (~18 MB). Install the **standalone executable** into `<TOOLS_DIR>` for portability.

### Recommended: standalone executable

```powershell
$tools = "<TOOLS_DIR>"   # recommended: ~/bin/videolink-to-article/
New-Item -ItemType Directory -Force -Path $tools | Out-Null
# Direct from GitHub. If TLS handshake fails, switch to the gh-proxy.com mirror below.
curl.exe -L --max-time 600 --retry 2 -o "$tools\yt-dlp.exe" `
  "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
# Mirror fallback for restrictive networks:
# curl.exe -L --max-time 600 --retry 2 -o "$tools\yt-dlp.exe" `
#   "https://gh-proxy.com/https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
& "$tools\yt-dlp.exe" --version
```

The standalone exe has Python embedded — no dependency on system Python. This makes it **portable across PATH registration**, unlike a venv shim which only works if the venv directory and Python interpreter remain at the same relative location.

### Alternative: isolated Python venv

Only use this if the standalone exe download keeps failing or if the agent already manages a Python venv for other reasons. Note that venv-installed `yt-dlp.exe` is a launcher shim that depends on the venv's Python interpreter — copying it to another location will break it.

```powershell
python -m venv "<TOOLS_DIR>\python-venv"
"<TOOLS_DIR>\python-venv\Scripts\pip.exe" install -U yt-dlp
"<TOOLS_DIR>\python-venv\Scripts\yt-dlp.exe" --version
```

When using this method, register `<TOOLS_DIR>\python-venv\Scripts` in PATH (NOT `<TOOLS_DIR>` itself), since the shim lives one level deeper.

### YouTube proxy

YouTube is typically inaccessible from Mainland China without a proxy. If the user has a local proxy (Clash/V2Ray/etc.):

```powershell
yt-dlp --proxy "http://127.0.0.1:7890" --list-subs "<URL>"
```

Common ports: Clash uses 7890, V2Ray uses 10809, etc. Ask the user if unsure.

---

## Persisting tools to PATH

Adding `<TOOLS_DIR>` to the user's persistent PATH is the **final step of every install procedure**. Without it, every new agent session has to re-discover the tools and may re-trigger the install flow.

### Windows (PowerShell, no admin required)

```powershell
$tools = "<TOOLS_DIR>"   # the same path you installed the binaries into
$current = [Environment]::GetEnvironmentVariable("Path", "User")
# Idempotent check: skip if already present
if (($current -split ';') -notcontains $tools) {
    $new = if ($current) { "$current;$tools" } else { $tools }
    [Environment]::SetEnvironmentVariable("Path", $new, "User")
    Write-Host "Added $tools to user PATH. Open a NEW PowerShell window to take effect."
} else {
    Write-Host "$tools is already on PATH."
}
```

The change takes effect in **new shells only** — already-open windows do not see the update. Verify in a fresh PowerShell:

```powershell
Get-Command BBDown
Get-Command yt-dlp
```

Both should resolve to the path inside `<TOOLS_DIR>`.

### POSIX (Linux / macOS)

Append to the user's shell rc file (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
TOOLS_DIR="$HOME/bin/videolink-to-article"
if ! echo "$PATH" | tr ':' '\n' | grep -qx "$TOOLS_DIR"; then
    echo "export PATH=\"$TOOLS_DIR:\$PATH\"" >> ~/.bashrc
    echo "Added $TOOLS_DIR to PATH in ~/.bashrc. Open a new shell or run 'source ~/.bashrc'."
fi
```

### Removing from PATH (uninstall)

When uninstalling the skill's tools:

```powershell
# Windows
$tools = "<TOOLS_DIR>"
$current = [Environment]::GetEnvironmentVariable("Path", "User")
$new = ($current -split ';' | Where-Object { $_ -ne $tools }) -join ';'
[Environment]::SetEnvironmentVariable("Path", $new, "User")
Remove-Item $tools -Recurse -Force
```

---

## Optional: ffmpeg

Installing real ffmpeg is **not required** for transcript extraction (subtitle-only workflow), but is needed if the user later wants to mux audio/video. Skip unless asked.

```powershell
winget install --id Gyan.FFmpeg -e
```

Or download a static build from https://www.gyan.dev/ffmpeg/builds/ and add to PATH.
