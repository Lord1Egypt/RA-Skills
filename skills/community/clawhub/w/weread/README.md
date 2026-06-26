# OpenClaw WeRead Skill

> OpenClaw skill for 微信读书 (WeRead) — fetch bookshelf, notes, highlights and reading stats.

[中文说明](#中文说明)

## What It Does

This skill gives your OpenClaw agent full access to your WeRead (微信读书) data:

- **Bookshelf** — list all books with progress, reading time, and completion status
- **Search** — fuzzy-match books by title or author
- **Book Info** — ratings, word count, publisher details
- **Reading Progress & Stats** — per-book progress, detailed time breakdowns
- **Highlights** — all your underlined passages
- **Notes / Thoughts** — your personal annotations
- **Best Reviews** — top community reviews
- **Chapters** — table of contents and chapter metadata
- **Cookie Verification** — check if your session is still active
- **Random Review** — pick random notes for daily review / morning reports
- **Notes Export** — bulk export all notes to structured local JSON files

## Prerequisites

- Python 3.9+
- [OpenClaw](https://github.com/nicepkg/openclaw) installed and configured
- A 微信读书 (WeRead) account with an active web session

## Installation

### Option 1: via clawhub (recommended)

```bash
clawhub install ChenyqThu/openclaw-weread-skill
```

### Option 2: manual clone

```bash
git clone https://github.com/ChenyqThu/openclaw-weread-skill.git \
  ~/.openclaw/workspace/skills/weread
```

## First-time Setup

The skill authenticates via a browser cookie stored at `~/.weread/cookie`.

### How to get your cookie

**Method 1 — Browser auto-extract (recommended):**

Ask your OpenClaw agent to open `https://weread.qq.com`, confirm you're logged in, then extract `document.cookie` and save it to `~/.weread/cookie`.

**Method 2 — Paste from DevTools:**

```bash
python3 ~/.openclaw/workspace/skills/weread/scripts/weread_login.py paste
```

Open WeRead in your browser → F12 → Network → pick any request → Headers → copy the `Cookie` value → paste when prompted.

**Method 3 — Direct write:**

If you already have the cookie string, write it directly:

```bash
mkdir -p ~/.weread
echo 'YOUR_COOKIE_STRING' > ~/.weread/cookie
chmod 600 ~/.weread/cookie
```

### Verify your cookie

```bash
python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py verify
```

> When the cookie expires, commands will return "Cookie 已过期". Simply re-do the setup above.

## Commands Reference

All commands output JSON to stdout. Errors go to stderr with exit code 1.

### Core API (`weread_api.py`)

| Command | Description | Example |
|---------|-------------|---------|
| `shelf` | List all books on your shelf | `python3 scripts/weread_api.py shelf` |
| `search <keyword>` | Fuzzy search books by title/author | `python3 scripts/weread_api.py search 心理学` |
| `info <bookId>` | Book details (rating, publisher, etc.) | `python3 scripts/weread_api.py info 123456` |
| `progress <bookId>` | Reading progress for a book | `python3 scripts/weread_api.py progress 123456` |
| `detail <bookId>` | Detailed reading stats (time breakdown) | `python3 scripts/weread_api.py detail 123456` |
| `bookmarks <bookId>` | All highlights / underlines | `python3 scripts/weread_api.py bookmarks 123456` |
| `reviews <bookId>` | Your notes / thoughts | `python3 scripts/weread_api.py reviews 123456` |
| `best-reviews <bookId> [N]` | Top N community reviews (default 10) | `python3 scripts/weread_api.py best-reviews 123456 5` |
| `chapters <bookId>` | Chapter list and metadata | `python3 scripts/weread_api.py chapters 123456` |
| `verify` | Check if cookie is still valid | `python3 scripts/weread_api.py verify` |

> **How to find `bookId`:** Run `shelf` or `search <keyword>` first — every result includes a `bookId` field you can pass to other commands.

### Random Review (`random_review.py`)

Pick random notes for daily review or morning reports:

```bash
python3 scripts/random_review.py --count 3 --min-length 50 --format text
```

| Flag | Default | Description |
|------|---------|-------------|
| `--count N` | 3 | Number of notes to pick |
| `--min-length L` | 20 | Minimum note length (filters short ones) |
| `--format` | text | Output format: `text` or `json` |

### Notes Export (`export_notes.py`)

Bulk export all notes to `~/.weread/`:

```bash
python3 scripts/export_notes.py            # full export
python3 scripts/export_notes.py --stats    # show statistics
```

### Login Helper (`weread_login.py`)

```bash
python3 scripts/weread_login.py paste      # paste cookie from DevTools
python3 scripts/weread_login.py chrome     # extract from Chrome (may need decryption)
```

## Morning Report Integration

The `random_review.py` script is designed to integrate with any morning/daily report system. Example:

```bash
# Pick 2 quality notes (min 50 chars) as JSON
python3 ~/.openclaw/workspace/skills/weread/scripts/random_review.py \
  --count 2 --min-length 50 --format json
```

You can pipe the output into your report generator, cron job, or agent workflow. Notes are weighted by length so more thoughtful annotations are more likely to be selected.

## Data Privacy

- All data is stored **locally** under `~/.weread/` — nothing is uploaded anywhere.
- Your cookie file (`~/.weread/cookie`) is created with `chmod 600` (owner-only read/write).
- The `.gitignore` in this repo explicitly excludes all user data files.
- No analytics, no telemetry, no third-party services.

## License

MIT

---

# 中文说明

## 功能概述

这是一个 OpenClaw 技能插件，让你的 AI 助手能够访问微信读书数据：

- 获取书架、搜索书籍、查看阅读进度和时长
- 获取划线、笔记、热门书评、章节信息
- 随机抽取读书笔记（可用于晨报/日报）
- 批量导出所有笔记到本地 JSON

## 安装

```bash
# 方式 1：通过 clawhub（推荐）
clawhub install ChenyqThu/openclaw-weread-skill

# 方式 2：手动安装
git clone https://github.com/ChenyqThu/openclaw-weread-skill.git \
  ~/.openclaw/workspace/skills/weread
```

## 首次配置

需要微信读书的浏览器 Cookie，存储在 `~/.weread/cookie`。

获取方式：
1. **浏览器自动提取**：让 OpenClaw 打开 weread.qq.com，提取 `document.cookie` 写入文件
2. **手动粘贴**：`python3 scripts/weread_login.py paste`，从浏览器 DevTools 复制 Cookie
3. **直接写入**：将 Cookie 字符串写入 `~/.weread/cookie`

验证：`python3 scripts/weread_api.py verify`

## 数据隐私

- 所有数据仅存储在本地 `~/.weread/` 目录
- Cookie 文件权限为 600（仅所有者可读写）
- 不上传任何数据，不包含任何分析或遥测
