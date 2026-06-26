---
name: video-fetch-download
version: 1.1.9
description: Download videos and torrents to cloud storage. Requires python3.12, rclone (115-fork, installed to ~/.local/bin), yt-dlp, and aria2c. Install via scripts/install.sh (installs all deps to user directory, no sudo; may append ~/.local/bin to PATH in shell profile). Writes credentials to ~/.config/rclone/rclone.conf (115 Pan, chmod 600) and ~/.config/video-fetch/quark_cookie.txt (Quark cookie, chmod 600) — stored locally only, never transmitted to third parties. Supports 115 offline download (server-side, zero local bandwidth), Quark Pan offline download and share link transfers, and 1000+ video site downloads via yt-dlp. Torrent search via Knaben API + apibay. Also supports Google Drive, OneDrive, Dropbox, and any rclone-compatible storage. Keywords: 离线下载, 下载视频, 磁力链, 种子, 夸克转存, 夸克离线, 115网盘, yt-dlp, 搜索电影, 磁力搜索.
---

# video-fetch-download

**中文简介：** 视频与种子下载神器，支持：①按片名搜索磁力链并一键提交115离线下载（`magnet_search.py`，支持中文片名自动转换，基于Knaben API + apibay双源）；②磁力链/种子URL通过115网盘离线下载（服务器端，不占本机带宽）；③夸克网盘磁力/URL离线下载；④夸克网盘分享链接一键转存；⑤YouTube/Bilibili/Twitter等1000+网站视频通过yt-dlp下载并上传至网盘，支持Google Drive、OneDrive、Dropbox等40+云存储。一键安装脚本（含SHA256校验），115支持扫码登录，夸克需手动提取一次Cookie（有效期数月）。

> ⚠️ **夸克说明：** 夸克网盘未开放扫码登录API，首次使用需从浏览器手动复制Cookie，操作约1分钟，之后数月内无需重复。

---

Download videos and torrents directly to cloud storage. Five input modes:

| Input | Tool | Destination | Bandwidth |
|---|---|---|---|
| Magnet / Torrent URL | 115 offline API | 115 Pan | Zero (server-side) |
| Magnet / URL | quark_offline.py | Quark Pan | Zero (server-side) |
| Quark share link | quark_save.py | Quark Pan | Zero (server-side) |
| Video URL (YT/Bili/etc.) | yt-dlp + rclone | 115 Pan | Local download |
| Local .torrent file | aria2c + rclone | 115 Pan | Local download |

---

## Installation

Run the one-command installer. It detects your OS/arch and installs all dependencies:

```bash
bash scripts/install.sh
```

Installs: `yt-dlp`, `rclone` (115-patched build), `aria2`, `python3.12`, `p115client`

> All binaries are verified with SHA256 checksums before installation.

---

## Authentication

### 115 Pan — QR code login (recommended, TV mode)

TV mode does not compete with your phone/browser sessions:

```bash
python3 scripts/115_qrlogin.py
# Scan the QR code with 115 App → confirm → done
# Credentials are saved securely to rclone config (chmod 600)
```

Re-login when cookie expires: `python3 scripts/115_qrlogin.py`

### Quark Pan — Cookie (manual, one-time setup)

> ⚠️ **Note:** Quark does not provide a public QR code login API.
> Authentication requires manually extracting a browser Cookie.
> The cookie is valid for several months and only needs to be set once.

**Steps:**
1. Open https://pan.quark.cn in a browser and log in
2. Press F12 → Network tab → Refresh the page
3. Click any request → Request Headers → Copy the `cookie` field
4. Run the setup wizard:

```bash
python3 scripts/quark_login.py
# Paste your cookie when prompted
# It is saved to ~/.config/video-fetch/quark_cookie.txt (chmod 600)
```

---

## Usage

### Search & submit to 115 (v1.1.3)

```bash
# Search only (Knaben API, auto-fallback to apibay)
python3 scripts/magnet_search.py "电影名"

# Search and auto-submit best result to 115
python3 scripts/magnet_search.py "电影名" --submit

# Submit specific result (e.g. #2)
python3 scripts/magnet_search.py "电影名" --submit --index 2

# Use apibay only
python3 scripts/magnet_search.py "Movie Name" --source apibay

# Merge results from both sources
python3 scripts/magnet_search.py "Movie Name" --source both
```

Supports Chinese titles (auto-mapped to English for search). Powered by Knaben API (primary) + apibay/TPB (fallback). Use `--source both` to merge results from both sources.

---

### Magnet link / Torrent URL → 115 offline download

```bash
python3.12 scripts/115_offline.py 'magnet:?xt=urn:btih:...'
python3.12 scripts/115_offline.py 'https://example.com/file.torrent'
python3.12 scripts/115_offline.py --list   # check task status
```

### Magnet link / URL → Quark offline download

```bash
python3 scripts/quark_offline.py 'magnet:?xt=urn:btih:...'
python3 scripts/quark_offline.py 'https://example.com/file.torrent'
python3 scripts/quark_offline.py --list   # check task status
python3 scripts/quark_offline.py --login  # show cookie setup instructions
```

### Quark share link → transfer to Quark Pan

```bash
python3 scripts/quark_save.py 'https://pan.quark.cn/s/xxxxxxxx'
python3 scripts/quark_save.py 'https://pan.quark.cn/s/xxxxxxxx' '/MyFolder'
python3 scripts/quark_save.py --list   # list Quark Pan root
```

### Video URL → download and upload to 115

```bash
VIDEOFETCH_REMOTE=115drive:云下载 bash scripts/video_fetch.sh 'https://youtube.com/watch?v=...'
```

### Local .torrent file → aria2c download and upload

```bash
bash scripts/video_fetch.sh /path/to/file.torrent 115drive:云下载
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `VIDEOFETCH_REMOTE` | `115drive:云下载` | rclone remote:path for uploads |
| `VIDEOFETCH_TMPDIR` | `/tmp/video-fetch` | local staging directory |

---

## Supported Sites

All sites supported by yt-dlp: YouTube, Bilibili, Twitter/X, Instagram, TikTok, Vimeo, and 1000+ more.

```bash
yt-dlp --list-extractors | grep -i <site>
```

---

## Other Cloud Storage

The skill uses rclone for uploads, which supports 40+ cloud storage providers. Any rclone-compatible remote works as a destination.

### Supported providers (examples)

| Provider | rclone backend | Auth method | Notes |
|---|---|---|---|
| Google Drive | `drive` | OAuth (browser link) | 15 GB free |
| Microsoft OneDrive | `onedrive` | OAuth (browser link) | Included with Microsoft 365 |
| Dropbox | `dropbox` | OAuth (browser link) | 2 GB free |
| PikPak | `pikpak` | OAuth (browser link) | Also supports server-side offline download |
| pCloud | `pcloud` | OAuth (browser link) | 10 GB free, Europe-based |
| Proton Drive | `protondrive` | Username + password + 2FA | Privacy-focused |
| Mega | `mega` | Username + password | 20 GB free, end-to-end encrypted |
| Backblaze B2 | `b2` | API key | Low-cost object storage |
| Amazon S3 | `s3` | API key | And 20+ S3-compatible providers |
| Any WebDAV | `webdav` | Username + password | Nextcloud, Owncloud, etc. |
| SFTP | `sftp` | SSH key or password | Any SSH server |

### Setup (one-time) — Recommended method

The easiest way to connect Google Drive (or any OAuth provider) to a headless server is to authorize on your **local machine** first, then copy the token to the server.

**Step 1 — On your local machine**, install rclone:
```bash
# macOS
brew install rclone

# Windows: download from https://rclone.org/install/

# Linux
curl https://rclone.org/install.sh | sudo bash
```

**Step 2 — Run the authorization wizard locally:**
```bash
rclone config
# → n (new remote)
# → name it: gdrive
# → type: drive (Google Drive)
# → leave client_id and client_secret blank (press Enter)
# → scope: 1 (full access)
# → browser will open automatically → log in → allow access
# → y (use auto config)
# → n (not a team drive, unless you need it)
# → q (quit)
```

**Step 3 — Copy the token to your server.**
On your local machine, find the token:
```bash
cat ~/.config/rclone/rclone.conf
# Find the [gdrive] section — copy the entire block
```

On your server, append it to rclone config:
```bash
cat >> ~/.config/rclone/rclone.conf << 'EOF'
[gdrive]
type = drive
token = {"access_token":"...","token_type":"Bearer",...}
EOF
```

**Step 4 — Verify:**
```bash
rclone lsd gdrive:
```

Once configured, use it as your download destination:
```bash
VIDEOFETCH_REMOTE=gdrive:Videos bash scripts/video_fetch.sh 'https://youtube.com/watch?v=...'
```

### Usage

```bash
# Download YouTube video → upload to Google Drive
VIDEOFETCH_REMOTE=gdrive:Videos bash scripts/video_fetch.sh 'https://youtube.com/watch?v=...'

# Download to OneDrive
VIDEOFETCH_REMOTE=onedrive:Downloads bash scripts/video_fetch.sh 'https://...'

# Download to Dropbox
VIDEOFETCH_REMOTE=dropbox:Videos bash scripts/video_fetch.sh 'https://...'
```

> **Note:** Downloads via yt-dlp use local bandwidth (file downloads to server first, then uploads to cloud). This differs from 115/Quark offline download which is server-side with zero local bandwidth.

---

## Re-authentication

| Service | Command |
|---|---|
| 115 Pan | `python3 scripts/115_qrlogin.py` |
| Quark Pan | `python3 scripts/quark_login.py` |

---

## Security

### Binary installation
- `yt-dlp` is downloaded from the official [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) repository and verified against the official `SHA2-256SUMS` file before installation. Installation is aborted if verification fails.
- `rclone` 115-fork is downloaded from [gaoyb7/rclone-release](https://github.com/gaoyb7/rclone-release) (a fork with 115 Pan backend support) with pinned SHA256 checksums for all supported architectures. Installation is aborted if verification fails.
- The rclone 115-fork is installed to `~/.local/bin/rclone` (user directory only). It does **not** replace or modify any system-level rclone installation.

### Credential handling
- 115 Pan credentials are obtained via QR code scan (TV mode) and written directly to the rclone config file (`chmod 600`). They are **never** passed as command-line arguments and are not visible in the process list (`ps aux`).
- Quark Pan cookie is manually extracted by the user from their own browser and stored at `~/.config/video-fetch/quark_cookie.txt` (`chmod 600`).
- All credentials are stored locally only and are **never** transmitted to any third party. They are only used to authenticate with the respective cloud service APIs (115 Pan, Quark Pan).

### Other
- `video_fetch.sh` does not use `--js-runtimes node` (no arbitrary JS execution via yt-dlp)
- Torrent search uses public APIs only (Knaben, apibay) — no credentials required

---

## Verified

- 115 offline download (magnet → 115 server) ✅
- 115 rclone direct access ✅
- Quark offline download (magnet → Quark server) ✅
- Quark share transfer ✅
- yt-dlp + rclone upload pipeline ✅
- aria2c torrent download ✅
- One-command installer (with SHA256 verification) ✅
- Dual search source: Knaben + apibay ✅
- Chinese title auto-mapping ✅
