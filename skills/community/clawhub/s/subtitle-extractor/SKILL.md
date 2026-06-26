---
name: Subtitle-Extractor
author: poltawa
version: 1.0.0
description: "Subtitle extractor for Bilibili, YouTube, Xiaohongshu, Douyin, and local files. Extracts native subtitles or Whisper transcription in original format. Agent handles dependency checking, file naming, and content analysis."

# 🔒 Security Declaration
# Downloads subtitles/audio from video platforms via yt-dlp.
# Cookie files are read locally only, never transmitted externally.
# No config files written. No secrets stored. No telemetry.
metadata:
  openclaw:
    requires:
      bins: ["yt-dlp"]
    behavior:
      networkAccess: indirect
      description: "Subtitle extractor for Bilibili, YouTube, Xiaohongshu, Douyin, and local files. Extracts native subtitles or Whisper transcription in original format. Agent handles dependency checking, file naming, and content analysis."
---

# Subtitle Extractor Skill

Extracts subtitles from video platforms in their native format. Supports Bilibili, YouTube, Xiaohongshu, Douyin, and local video files.

**Scope of this skill:** subtitle extraction only. Summarization, analysis, Q&A — all handled by the agent based on the user's actual request.

---

## What It Does

1. Detect platform from URL
2. Extract native subtitles via yt-dlp (or Whisper transcription when no native subtitles exist)
3. Output: raw subtitle file path + video title/author
4. Agent saves subtitle to `outputs/` and processes per user request

---

## Dependencies

Agent must verify dependencies before calling the script. If any are missing, inform the user with the relevant install command.

### yt-dlp — Required (always)

```bash
# Check
yt-dlp --version

# Install
pip install yt-dlp                    # all platforms (recommended)
brew install yt-dlp                   # macOS Homebrew
winget install yt-dlp.yt-dlp         # Windows WinGet
scoop install yt-dlp                  # Windows Scoop
conda install -c conda-forge yt-dlp  # Conda environments

# Upgrade existing install
pip install -U yt-dlp
```

### ffmpeg — Required only for Whisper transcription

> Only needed for Xiaohongshu, Douyin, local files, or Path B (Whisper transcription).

```bash
# Check
ffmpeg -version

# Install
brew install ffmpeg                   # macOS Homebrew
winget install Gyan.FFmpeg           # Windows WinGet
choco install ffmpeg                  # Windows Chocolatey
scoop install ffmpeg                  # Windows Scoop
apt install ffmpeg                    # Ubuntu / Debian
dnf install ffmpeg                    # Fedora / RHEL (may need RPM Fusion)
pacman -S ffmpeg                      # Arch Linux
snap install ffmpeg                   # Ubuntu Snap
```

> **Windows users:** restart the terminal after installation for PATH to take effect.
> If `winget` is unavailable, download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin/` directory to system PATH.

### faster-whisper — Required only for transcription platforms

> Only needed for Xiaohongshu, Douyin, local files, or Path B (Whisper transcription).

```bash
# Check
python3 -c "from faster_whisper import WhisperModel; print('ok')"

# Install
pip install faster-whisper

# Configure model size (default: base)
export VIDEO_SUMMARY_WHISPER_MODEL=base   # tiny | base | small | medium | large
```

**Note:** Model files are downloaded automatically on first transcription run (~150MB for base). This may take a minute depending on network speed.

**China network note:** If auto-download fails (HuggingFace blocked), see [Whisper model download failed](#whisper-model-download-failed) in Troubleshooting.

**Transcription time estimate (CPU, faster-whisper):**

| Video Duration | tiny | base | small | medium |
|---------------|------|------|-------|--------|
| 5 min  | ~10s | ~20s | ~40s  | ~80s   |
| 15 min | ~30s | ~60s | ~2m   | ~4m    |
| 30 min | ~60s | ~2m  | ~5m   | ~10m   |

GPU accelerates transcription 5–15×. First run downloads the model (~150MB for base).

---

## Cookie Configuration

### Bilibili — Cookie Required

Bilibili requires a cookie file for all requests. The script auto-discovers cookie files **in the skill directory only** (same folder as `subtitle-extractor.py` and `SKILL.md`):

Any `.txt` file whose name contains `bilibili` will be picked up automatically — including the browser extension's default export format `www.bilibili.com_netscape_<timestamp>.txt`.

**Place your cookie file in the skill directory.** The agent does not need to locate or pass it manually (see Step 1b).

### Xiaohongshu / Douyin — Manual

```bash
video-summary "https://www.xiaohongshu.com/explore/xxxxx" --cookies cookies.txt
# or
export VIDEO_SUMMARY_COOKIES=/path/to/cookies.txt
```

**How to export cookies:**
1. Install browser extension: "Cookie Editor（https://cookieeditor.org/）"
2. Log in to the platform
3. Export cookies to a `.txt` file（Netscape format）

---

## Agent Workflow

### EXECUTION ORDER — NON-NEGOTIABLE

Steps 1–4 in this skill MUST be completed in full before addressing any user request. The subtitle file MUST be saved to disk (Step 4) before the agent proceeds to summarization, translation, analysis, or any other task the user has asked for.

Treat Steps 1–4 as mandatory prerequisites, not optional helpers. Do not skip any step even if the user's final output format (e.g. a markdown file) appears to make it unnecessary.

### Step 1 — Check Dependencies

```bash
yt-dlp --version
```

If the user requests Whisper transcription (keywords: "whisper转录" / "用whisper" / "transcribe" / "转录" / "语音转文字"), or the platform is Xiaohongshu, Douyin, or a local file, also check:

```bash
ffmpeg -version
python3 -c "from faster_whisper import WhisperModel; print('ok')"
```

If anything is missing, stop and tell the user which dependency to install (see Dependencies section).

### Step 1b — Bilibili Cookie

The script auto-discovers any `.txt` file containing "bilibili" in the skill directory. Do not search for or pass the cookie file yourself.

Only act if the script exits with:
- `未找到 Bilibili Cookie 文件` → tell the user to place a cookie file in the skill directory
- `Bilibili 412 错误：Cookie 已过期` → tell the user to re-export

To export: install "Cookie Editor (https://cookieeditor.org/)", log in to Bilibili, export Netscape format → place in skill directory → retry.

### Step 2 — Extract Subtitles

Determine which path applies, then execute it completely before moving to Step 3.

---

**Path A — Native subtitles**

Use when: Bilibili or YouTube URL, and the user has not mentioned any transcription keyword.

Tell the user: "正在提取字幕..."

```bash
python subtitle-extractor.py "<url>"              # auto-detect language
python subtitle-extractor.py "<url>" --lang zh-CN  # force language
```

Parse the JSON from stdout. You now have all four fields needed for Step 3:

| Field | Value |
|---|---|
| `title` | from this JSON |
| `author` | from this JSON |
| `platform` | from this JSON |
| `subtitle_file` | from this JSON |

If the script exits non-zero: read stderr, report the error to the user, stop.

---

**Path B — Whisper transcription**

Use when: user mentions any transcription keyword, OR platform is Xiaohongshu or Douyin.

> Transcription keyword takes priority over phrasing like "提取字幕" or "字幕原文" — those describe the desired output, not the method.

**Call 1 — Download audio** (skip for local files, go to Call 2 directly)

Tell the user: "正在下载音频，请稍候..."

```bash
python subtitle-extractor.py "<url>" --step download-audio
```

Parse the JSON from stdout and record these values:

| Field | Value |
|---|---|
| `title` | from this JSON |
| `author` | from this JSON |
| `platform` | from this JSON |
| `audio_file` | from this JSON — input for Call 2 |

If the script exits non-zero: read stderr, report the error to the user, stop.

Tell the user: "音频下载完成，开始 Whisper 转录（模型: base），请稍候..."

**Call 2 — Transcribe**

For URL input, use the `audio_file` recorded from Call 1:
```bash
python subtitle-extractor.py "<audio_file>" --step transcribe
```

For local file input (set `title` = filename, `author` = "local"):
```bash
python subtitle-extractor.py "<local_file_path>" --step transcribe
```

Parse the JSON from stdout and record:

| Field | Value |
|---|---|
| `subtitle_file` | from this JSON |

Tell the user: "转录完成！"

If the script exits non-zero:
- Read stderr, report the error to the user, stop
- If stderr contains `Whisper 模型下载失败`: show the full error message verbatim — it contains the exact download directory and manual steps

---

**Failure rule:** Do not run yt-dlp, ffmpeg, or Whisper commands manually. Do not retry with different flags unless the error message explicitly says to.

### Step 3 — Confirm Data

Verify you have collected all four values from the script outputs in Step 2:

| Field | Path A source | Path B source |
|---|---|---|
| `title` | script JSON | Call 1 JSON (or filename for local) |
| `author` | script JSON | Call 1 JSON (or "local") |
| `subtitle_file` | script JSON | Call 2 JSON |

Note: non-ASCII characters in JSON output appear as `\uXXXX` escapes — standard JSON parsing produces the correct decoded strings.

### Step 4 — Save Subtitle to Outputs (REQUIRED — DO NOT SKIP)

Before answering the user, save the subtitle file to the session outputs directory.

**Naming rule: `{title前8字}_{author}.{原格式扩展名}`**

Steps:
1. Take `title`, keep the first **8 characters** (Chinese and English each count as 1)
2. Replace unsafe filesystem characters `/ \ : * ? " < > |` and spaces with `_`
3. Apply the same sanitization to `author`
4. Use the extension from `subtitle_file` path (`.srt` or `.vtt`)
5. Save to `{outputs_dir}/{safe_title8}_{safe_author}.{ext}`


### Step 5 — Process and Respond

Read the subtitle file content and respond to the user's original request — summarize, analyze, translate, answer questions, etc. The subtitle content is in SRT or VTT format with timestamps; LLMs handle both directly.



## Platform Notes

| Platform | Method | Notes |
|----------|--------|-------|
| **YouTube** | yt-dlp native CC + auto-generated | Best support, usually no cookies needed |
| **Bilibili** | yt-dlp native CC | Auto-discovers cookies; zh-CN → ai-zh fallback; 412 error handling |
| **Xiaohongshu** | Whisper transcription | No native subtitles; requires ffmpeg + whisper |
| **Douyin** | Whisper transcription | No native subtitles; requires ffmpeg + whisper |
| **Local files** | Whisper transcription | mp4, mkv, webm, mp3, etc. |

### Supported URL Formats

**YouTube:** `youtube.com/watch?v=...` · `youtu.be/...`

**Bilibili:** `bilibili.com/video/BV...` · `bilibili.com/video/av...` · `b23.tv/...` (short link)

**Xiaohongshu:** `xiaohongshu.com/explore/...` · `xhslink.com/...` (short link)

**Douyin:** `douyin.com/video/...` · `v.douyin.com/...` (short link)

---

## Script Reference

```
Usage:
    python subtitle-extractor.py <url|file> [options]

Steps (--step):
    download-audio    Download audio from URL → {"audio_file", "title", "author", "platform"}
    transcribe        Transcribe local audio/video file → {"subtitle_file"}
    (none)            Extract native subtitles (default path) → {"title", "author", "platform", "subtitle_file"}

Options:
    --step <name>     Pipeline step to run: download-audio | transcribe
    --lang <code>     Subtitle language code, default path only (default: auto)
    --cookies <file>  Cookie file for restricted content
    --help            Show help

Environment Variables:
    VIDEO_SUMMARY_COOKIES        Path to cookies file
    VIDEO_SUMMARY_WHISPER_MODEL  Whisper model size (default: base)
```

---

## Troubleshooting

### "yt-dlp: command not found"
```bash
pip install yt-dlp
```

### "No subtitles found"
- The video may not have CC subtitles — use Path B (`--step download-audio` then `--step transcribe`) to force Whisper
- For Xiaohongshu/Douyin, transcription is always required (no native subtitles)
- Try `--lang` to specify a different language code

### Bilibili 412 Precondition Failed
Cookie expired. Re-export:
1. Log in to Bilibili in browser
2. Use "Cookie Editor（https://cookieeditor.org/）" extension
3. Export（Netscape format）→ place in skill directory → retry

### Bilibili: no zh-CN subtitle found
The script automatically falls back to `ai-zh`. If both fail, it lists all available subtitle codes. Use `--lang <code>` to specify one.

### "Whisper not installed"
```bash
pip install faster-whisper
```

### Whisper model download failed

The script tries `hf-mirror.com` then `huggingface.co`. If both fail (common in China), the script will print exact steps. **Show the error message to the user verbatim** — it contains the exact directory path and download URL.

Manual download (browser accessible in China):
1. Open: `https://modelscope.cn/models/pkufool/faster-whisper-base/files`
2. Download these 5 files: `config.json` `model.bin` `tokenizer.json` `vocabulary.json` `preprocessor_config.json`
3. Create the directory shown in the error message and place all 5 files there
4. Re-run the script — it auto-detects the local model, no download needed

For other model sizes (tiny/small/medium/large), change `faster-whisper-base` to `faster-whisper-{size}` in the ModelScope URL.

### "ffmpeg not found" (during transcription)
See ffmpeg install commands in the Dependencies section above.

### Video too long for Whisper
Use a smaller model:
```bash
export VIDEO_SUMMARY_WHISPER_MODEL=tiny
```

---

*Extract subtitles. Let the agent think.*
