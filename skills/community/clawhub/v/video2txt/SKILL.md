---
name: video-transcript
version: 1.0.0
description: Extract transcripts/subtitles from video URLs and deliver as .docx files. Use this skill whenever the user provides a video link (YouTube, Bilibili, or any yt-dlp supported platform) and asks for a transcript, subtitles, lecture notes, or spoken content in text form. Also trigger when user says "帮我把这个视频转成文字", "视频讲稿", "字幕文档", "transcript", "lecture notes from video", or pastes a video URL with any request to get the text content.
compatibility:
  tools:
    - exec
  dependencies:
    - name: yt-dlp
      install: "pip install yt-dlp  # or: winget install yt-dlp"
      check: "yt-dlp --version"
    - name: node
      install: "https://nodejs.org"
      check: "node --version"
    - name: docx (npm, local)
      install: "cd ~/.agents/skills/video-transcript/scripts && npm install"
      check: "node -e \"require('./node_modules/docx')\""
---

# Video Transcript Skill

Extract subtitles from a video URL and deliver clean .docx transcript files.
For non-Chinese videos, produce two files: original language + Chinese translation.
For Chinese videos, produce one file.

## Workflow

### Step 0 — First-time setup (once only)

Check if `node_modules` exists in the scripts directory. If not, run:

```powershell
$skillScripts = "$env:USERPROFILE\.agents\skills\video-transcript\scripts"
if (-not (Test-Path "$skillScripts\node_modules\docx")) {
    Push-Location $skillScripts
    npm install
    Pop-Location
}
```

### Step 1 — Download subtitles with yt-dlp

Run in a temp directory (use `$env:TEMP\vt_<random>` on Windows):

```powershell
$tmp = "$env:TEMP\vt_$(Get-Random)"
New-Item -ItemType Directory -Force $tmp | Out-Null
```

**YouTube:**
```powershell
# Try manual subs first, fall back to auto-generated
yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "en,zh-Hans,zh-Hant,zh" --convert-subs srt -o "$tmp\sub" "<URL>"
```

**Bilibili:**
```powershell
yt-dlp --skip-download --write-subs --sub-langs "zh-Hans,zh,ai-zh" --convert-subs srt -o "$tmp\sub" "<URL>"
```

**Other platforms:** Use the same YouTube command — yt-dlp handles most platforms automatically.

After download, list what was fetched:
```powershell
Get-ChildItem $tmp -Filter "*.srt"
```

### Step 2 — Detect available subtitle files

Pick the best available file:
- Prefer manual subs over auto-generated (`.en.srt` over `.en-orig.srt` or `.en-auto.srt`)
- For Bilibili: pick `zh-Hans` or `ai-zh`
- If multiple languages exist, note them all

If NO subtitle file was downloaded:
- Tell the user: "该视频没有可用字幕，yt-dlp 无法提取文字内容。如需转录请使用 Whisper 语音识别（需额外安装）。"
- Stop here.

### Step 3 — Parse SRT to plain text

Read the .srt file and strip all timing/index lines. Keep only the spoken text lines.

SRT format to strip:
```
1
00:00:01,000 --> 00:00:03,500
This is the spoken text.

2
00:00:04,000 --> 00:00:06,000
More text here.
```

Output: plain text, one paragraph per subtitle block, blank lines between blocks removed (merge into flowing paragraphs). Also strip HTML tags like `<i>`, `<b>`, `<font ...>`.

Do this parsing yourself by reading the file content — no external tool needed.

### Step 4 — Translate if needed

Detect the subtitle language:
- If **Chinese** (zh, zh-Hans, zh-Hant): skip translation, one file only
- If **other language**: translate the full plain text to Chinese using your own translation capability

Translation guidelines:
- Produce natural, readable Chinese — not word-for-word
- Preserve paragraph structure
- Keep proper nouns, technical terms transliterated or explained inline if needed
- Do NOT add commentary or summaries — pure translation only

### Step 5 — Generate .docx files

Use the bundled script. The script path is:
`~/.agents/skills/video-transcript/scripts/make_docx.js`

Get the video title from yt-dlp output or use a sanitized version of the URL as fallback.

**For non-Chinese video (two files):**
```powershell
# Original
node "~/.agents/skills/video-transcript/scripts/make_docx.js" "$tmp\transcript_original.docx" "<VideoTitle> - Original" "<plain_text>"

# Chinese translation
node "~/.agents/skills/video-transcript/scripts/make_docx.js" "$tmp\transcript_zh.docx" "<VideoTitle> - 中文译稿" "<chinese_text>"
```

**For Chinese video (one file):**
```powershell
node "~/.agents/skills/video-transcript/scripts/make_docx.js" "$tmp\transcript_zh.docx" "<VideoTitle> - 讲稿" "<plain_text>"
```

For long texts, write content to a temp `.txt` file first and pipe it:
```powershell
$plain | Out-File -Encoding utf8 "$tmp\content.txt"
Get-Content "$tmp\content.txt" -Raw | node "~/.agents/skills/video-transcript/scripts/make_docx.js" "$tmp\transcript_original.docx" "<title>"
```

### Step 6 — Deliver to user

Tell the user the output file paths clearly:
- "原文讲稿：`C:\...\transcript_original.docx`"
- "中文译稿：`C:\...\transcript_zh.docx`"

Optionally show a short preview (first 200 chars) of the extracted text so the user can verify quality.

## Error handling

| Situation | Action |
|---|---|
| No subtitles found | Inform user, suggest Whisper as alternative |
| yt-dlp not found | `yt-dlp --version` to check; tell user to install if missing |
| node/docx error | Show error, check if `docx` npm package is installed globally |
| Private/geo-blocked video | Inform user the video is inaccessible |

## Notes

- Always clean up `$tmp` dir after delivering files, or leave it and tell the user the path
- The `make_docx.js` script resolves `docx` from global npm automatically
- For very long videos, translation may take a moment — let the user know
