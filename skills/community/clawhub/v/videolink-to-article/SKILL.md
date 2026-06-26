---
name: videolink-to-article
description: Use when the user provides a Bilibili or YouTube URL and asks for a transcript, article, or subtitle extraction. Downloads platform subtitles via BBDown / yt-dlp and produces a clean Markdown transcript in the source language.
---

# Videolink To Article

Extract subtitles from a Bilibili or YouTube video URL and process them into a clean, structured Markdown transcript. Handles tool installation, subtitle download, metadata extraction, and a deterministic-then-interpretive cleanup pipeline that preserves the speaker's original wording.

## When To Use

Trigger on Bilibili (`bilibili.com/video/BV...`, `b23.tv/...`) or YouTube (`youtube.com/watch?v=...`, `youtu.be/...`) URLs combined with requests for transcripts, articles, subtitle extraction, or restructuring spoken content into Markdown. Do **not** trigger for: download-only requests, audio-only ASR (no subtitles available; use a Whisper-based skill), or non-{Bilibili,YouTube} platforms.

## Routing

| URL pattern | Tool |
|---|---|
| `bilibili.com/video/BV...`, `b23.tv/...` | BBDown |
| `youtube.com/watch?v=...`, `youtu.be/...` | yt-dlp |
| Other | Decline |

## Directory Conventions

| Placeholder | Purpose | Lifetime |
|---|---|---|
| `<TOOLS_DIR>` | Persistent binary cache (BBDown, yt-dlp, helper scripts). | Cross-session. |
| `<WORK_DIR>`  | Per-task outputs (SRT, metadata.json, transcript). | Single task. |

**Choosing `<TOOLS_DIR>`** (apply in order, stop at first match):
1. Reuse the agent's existing binary cache directory (`binaries/`, `bin/`, `tools/` under per-user data) as `<that-dir>/videolink-to-article/`.
2. Otherwise OS default — Windows: `~/bin/videolink-to-article/`; macOS: `~/Library/Application Support/videolink-to-article/bin/`; Linux: `~/.local/bin/videolink-to-article/`.
3. Never use a workspace folder, system temp, or cache-style dir — tools must survive across sessions.
4. After install, register `<TOOLS_DIR>` on the user's persistent PATH (see `references/install_tools.md` § Persisting tools to PATH). Without this, every new session re-runs the install probe.

**`<WORK_DIR>`** is per-task. Reasonable picks: workspace-relative `output/` or `transcripts/`, or a task-named subfolder under temp. Safe to clean up after delivery.

---

## Step 1: Verify Tools

For Bilibili check `BBDown.exe`; for YouTube check `yt-dlp.exe`. Probe order: system PATH → `<TOOLS_DIR>/<exe>` → any path the user has explicitly mentioned. If missing, install per `references/install_tools.md` (use the **standalone yt-dlp.exe**, not a venv shim) and end the install with PATH registration.

BBDown does a startup check for `ffmpeg`. If ffmpeg is missing, pass `--ffmpeg-path "<any-existing-exe>"` (e.g. `<TOOLS_DIR>/yt-dlp.exe`). Subtitle-only mode never actually invokes ffmpeg, but BBDown refuses to start without the path resolving.

YouTube from Mainland China usually requires `--proxy http://127.0.0.1:<port>`.

---

## Step 2: Identify Video (fetch metadata)

```bash
python scripts/fetch_metadata.py "<URL>" --bbdown "<bbdown.exe>" --ytdlp "<yt-dlp.exe>" --ffmpeg-path "<any-existing-exe>"
```

Save stdout JSON to `<WORK_DIR>/<video_id>/metadata.json`. Fields: `platform`, `video_id`, `title`, `uploader`, `uploader_url`, `duration_seconds`, `publish_date`, `url`. Notes:
- Bilibili `uploader` may be `null` (BBDown's `--only-show-info` doesn't print UP name); extract from title or ask the user.
- Exit `3` = title parse failed → upstream tool's output format changed.

Use `<video_id>` to name the per-task subdirectory under `<WORK_DIR>`.

---

## Step 3: Probe Available Subtitles

Always list before downloading.

**Bilibili:**

```powershell
BBDown.exe "<URL>" --only-show-info --sub-only --skip-ai false `
  --ffmpeg-path "<any-exe>" *> bbdown_info.log 2>&1
Get-Content bbdown_info.log -Encoding UTF8
```

> ⚠️ **`--skip-ai false` is required** every time — BBDown's default skips AI subtitles silently. The double-negative is intentional; verify the argument is present.

If the log shows "需要登录", run `BBDown.exe login` first (see `references/auth.md`).

**YouTube:**

```bash
yt-dlp --list-subs --skip-download "<URL>"
```

If the command fails with an authentication error (e.g. "Sign in to confirm you're not a bot", "Sign in to confirm your age", HTTP 403), follow this auth resolution flow **in order**, stopping at the first success:

1. **Try `--cookies-from-browser`** (fastest if it works):
   ```powershell
   yt-dlp --cookies-from-browser edge --list-subs --skip-download "<URL>"
   ```
   If this fails with `Could not copy Chrome cookie database` → close all browser instances and retry. If it fails with `Failed to decrypt with DPAPI` (App-Bound Encryption on Chromium ≥ v127), **skip to step 2** — this error is unrecoverable.

2. **Ask the user for a `cookies.txt` file.** This is the most reliable method. Present the following guidance to the user:

   > YouTube 需要登录态才能获取字幕，但自动读取浏览器 Cookie 失败了。
   >
   > 请按以下步骤导出 `cookies.txt` 文件：
   > 1. 安装 Chrome 扩展 [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)（开源、本地运行、无遥测）
   > 2. 在浏览器中打开目标 YouTube 视频页面（确保已登录）
   > 3. 点击扩展图标 → **Export**，将 `cookies.txt` 保存到本地
   > 4. 告诉我 cookies.txt 文件的路径

   Once the user provides the file path, pass it to yt-dlp:
   ```bash
   yt-dlp --cookies "<cookies.txt_path>" --list-subs --skip-download "<URL>"
   ```

   Save the cookies path for reuse in Step 4.

Three caption kinds, ranked by quality:

| Entry | Meaning | Quality |
|---|---|---|
| `Available subtitles` | Human-uploaded | Highest |
| `Available automatic captions` → `<lang>-orig` | Source-language ASR | High (no translation step) |
| `Available automatic captions` → `<lang>` | Auto-translation of source ASR | Lower (machine translation) |

**Picking rule.** Prefer human captions; otherwise prefer `<lang>-orig`; only fall back to translated auto-captions when neither exists. Trap: if you see e.g. `zh-Hans` and `en-orig` but no `zh-Hans-orig`, the speaker is **not** speaking Chinese — `zh-Hans` is a translation of the English ASR. Always download `<lang>-orig` and work from it; do not pre-emptively prefer a translated track because it matches the user's interface language.

---

## Step 4: Download Subtitles

Layout: `<WORK_DIR>/<video_id>/{metadata.json, *.srt, sentences.txt}`.

**Bilibili:**

```powershell
BBDown.exe "<URL>" --sub-only --skip-ai false `
  --work-dir "<WORK_DIR>/<video_id>" --ffmpeg-path "<any-exe>"
```

Output: `<videoTitle>.<lang>.srt` (e.g. `*.ai-zh.srt`, `*.ai-en.srt`).

**YouTube:**

```bash
yt-dlp --write-subs --write-auto-subs \
  --sub-langs "<source-lang>-orig,<source-lang>" \
  --convert-subs srt --skip-download --ignore-no-formats-error \
  -o "<WORK_DIR>/<video_id>/%(id)s.%(ext)s" "<URL>"
```

If Step 3 resolved auth via `--cookies-from-browser`, add the same flag here. If a `cookies.txt` file was provided, add `--cookies "<cookies.txt_path>"`. Example with cookies:

```bash
yt-dlp --cookies "<cookies.txt_path>" \
  --write-subs --write-auto-subs \
  --sub-langs "<source-lang>-orig,<source-lang>" \
  --convert-subs srt --skip-download --ignore-no-formats-error \
  -o "<WORK_DIR>/<video_id>/%(id)s.%(ext)s" "<URL>"
```

Replace `<source-lang>` with the actual language code from Step 3 — do not hardcode a default. The `-o` template uses `%(id)s` (not `%(title)s`) on purpose: titles vary in punctuation and special characters, and yt-dlp's title sanitization differs from BBDown's; using `id` keeps file naming uniform across both platforms, and the human-readable title prefix is added later by Step 8 (`rename_with_title.py`). **`--ignore-no-formats-error` is required**: without it, yt-dlp aborts on `Requested format is not available` *before* writing queued subtitle files (common on bot-flagged sessions). Add `--proxy http://127.0.0.1:<port>` when blocked.

**Fallback for srv3.** If yt-dlp writes `*.srv3` instead of `*.srt` (its converter pipeline can't always handle srv3 without ffmpeg), run `python scripts/srv3_to_text.py <input.srv3> <out_basename>` to produce `.srt` and `.txt` directly. Stdlib-only.

For auth-required videos (member-only, age-restricted, "Sign in to confirm you're not a bot"), see `references/auth.md`.

---

## Step 5: Validate the SRT

```powershell
Get-Content "<file>.srt" -Encoding UTF8 -TotalCount 30
```

| Symptom | Cause | Action |
|---|---|---|
| 0-byte file | Lang not actually available | Retry Step 3/4 with another lang code |
| Timestamps all `00:00:00,000` | Corrupt subtitle | Re-download |
| Garbled / mojibake | Wrong encoding | Re-read with UTF-8 |
| Body is `[音乐]` / `[Music]` only | No real captions | Stop; tell the user |
| Segment count ≪ video length | Truncated | Retry |

---

## Step 6: Normalize SRT (deterministic)

```bash
python scripts/srt_to_sentences.py <input.srt> <WORK_DIR>/<video_id>/sentences.txt [--target-len 60] [--max-len 120]
```

Defaults work for typical conversational video. Dense expository → raise `--max-len` (e.g. 180). Staccato delivery → lower `--target-len` (e.g. 40). Exit `2` = empty / no parseable segments → SRT is invalid; revisit Step 5.

---

## Step 7: Interpretive Cleanup & Restructure

### Output language (hard rule)

**The transcript stays in the source language of the video.** English video → English transcript; Japanese → Japanese; Mandarin → Mandarin. **Do not silently translate** to the user's interface language, the agent's response language, or any other locale.

Translate only when the user **explicitly** asks ("整理成中文文稿", "translate to English"). Even then, produce the source-language version first as the primary deliverable; offer translation as an additional output.

This rule overrides any default-language hint injected into the agent's runtime context.

### Cleanup checklist

1. **Preserve original wording.** Do not paraphrase. The transcript should read like the speaker's own words, with errors fixed and filler removed.
2. **Fix ASR errors.** Scan the full transcript once, build a per-video glossary (cross-reference video title / description / channel name / web search), then apply consistently. Apply only when the error is unambiguous and the correct form is verifiable. Methodology + worked example: `references/cleanup_guide.md`.
3. **Remove filler sparingly.** Read § Words to KEEP first — many seemingly-filler words carry the speaker's stance. The lists are organized by language; consult the section matching the source language.
4. **Add lightweight headings.** Insert `##` / `###` only at obvious topic transitions the speaker explicitly signals ("第一个是…", "Let's talk about…", "Moving on to…"). Headings stay in the source language, short, descriptive. **No structural signals → no headings.** Output continuous paragraphs.
5. **Final structure.** Use `metadata.json` from Step 2 to populate the header. Header label set follows the source language (Chinese labels for Chinese videos, English for English, etc.). Templates: `references/cleanup_guide.md` § Output Skeleton Template.

### What the deliverable must NOT contain

- "整理说明" / "Changes applied" tables
- Footnote citations for ASR-corrected passages (`[^1]: 出自...`)
- Confidence/uncertainty annotations or `[？...]` placeholders
- Tool-internal notes about the cleanup process
- Any content the speaker did not say

When a fragment cannot be cleaned with confidence, **trim** it rather than guess or annotate. Full rule list: `references/cleanup_guide.md` § What NOT To Do.

---

## Step 8: Rename final transcript & cleanup

After Step 7 has written `transcript.md` (and any `transcript_*.md` translations), run:

```bash
python scripts/rename_with_title.py <WORK_DIR>/<video_id>
```

This renames the final transcript file(s) to include the sanitized video title as a prefix, while keeping `<video_id>` as a stable suffix. Result format: `<sanitized_title>__<video_id>.md`. The script is idempotent — safe to re-run.

**Cleanup intermediate files.** After renaming, delete all intermediate artifacts (`.srt`, `.srv3`, `sentences.txt`, `.info.json`, `metadata.json`, etc.) — only the final renamed transcript(s) should remain in the output directory. The agent should deliver only the final transcript file to the user.

```powershell
# Example cleanup (Windows PowerShell) — keep only the renamed transcript(s)
Get-ChildItem "<WORK_DIR>/<video_id>" -File | Where-Object {
    $_.Name -notlike "*__*.md"
} | Remove-Item -Force
```

**Why rename only the transcript.** Since intermediate files (SRT, sentences.txt, metadata.json) are cleaned up and not delivered, the rename logic only needs to handle the final `transcript.md` and any translation variants (`transcript_*.md`). This keeps the output directory clean with just the deliverable(s).

---

## Troubleshooting

`references/troubleshooting.md` is a recovery matrix organized by failure category (tools & environment, network & download, authentication, subtitle availability, encoding & display). Always retry once before reporting transient network issues.

---

## Resources

**scripts/**
- `fetch_metadata.py` — unified Bilibili/YouTube metadata fetcher (JSON to stdout). Exit 1 (URL invalid) / 2 (tool missing) / 3 (parse failed).
- `srt_to_sentences.py` — deterministic SRT preprocessor; merges short segments into sentence-like lines. Exit 2 on empty/invalid input.
- `srv3_to_text.py` — fallback converter when yt-dlp's `--convert-subs srt` leaves you with raw srv3 XML. Stdlib-only. Exit 2 on empty input.
- `rename_with_title.py` — Step 8 helper: renames the final transcript file(s) with a sanitized video title prefix. Stdlib-only, idempotent. Exit 2 (metadata.json missing) / 3 (metadata.json missing fields).

**references/**
- `install_tools.md` — install procedures for BBDown / yt-dlp (Windows + POSIX), GitHub mirrors, ffmpeg workaround, PATH registration.
- `auth.md` — authentication flows: BBDown QR-code login, yt-dlp `--cookies-from-browser`, manual `cookies.txt` export. App-Bound Encryption pitfalls.
- `cleanup_guide.md` — methodology for Step 7: ASR error identification, Words to KEEP vs filler, sectioning heuristics, output skeleton.
- `worked_example.md` — one full walkthrough on a real video. Read once when learning; skip when you just need rules.
- `troubleshooting.md` — recovery matrix.
