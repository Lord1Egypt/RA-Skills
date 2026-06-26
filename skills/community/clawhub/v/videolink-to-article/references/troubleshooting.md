# Troubleshooting

Recovery matrix for `videolink-to-article`. Substitute placeholders (`<TOOLS_DIR>`, `<WORK_DIR>`) per SKILL.md § Directory Conventions. **Always retry once** before reporting transient network issues.

---

## Tool & environment

| Symptom | Cause | Recovery |
|---|---|---|
| `BBDown` exits "找不到可执行的ffmpeg文件" | Startup ffmpeg check fails | Add `--ffmpeg-path "<TOOLS_DIR>/yt-dlp.exe"` (any existing exe works as placeholder). |
| `yt-dlp: command not found` after install | `<TOOLS_DIR>` not on PATH | Run `install_tools.md` § Persisting tools to PATH; **open a new shell** (existing shells don't see the update). |
| `winget` exits 1 silently | Network/permission | Skip winget; use the gh-proxy.com block in `install_tools.md` § Method C. |

## Network & download

| Symptom | Cause | Recovery |
|---|---|---|
| `curl: (35) schannel: failed to receive handshake` | GitHub release CDN blocked | Wrap URL with `https://gh-proxy.com/`. Fallbacks: `ghproxy.net`, `mirror.ghproxy.com`. |
| yt-dlp times out on YouTube | No proxy in restricted region | Add `--proxy "http://127.0.0.1:<port>"` (Clash 7890, V2Ray 10809; ask user). |
| BBDown stalls mid-download | Bilibili rate-limit | Wait 30s; retry. Persistent → add `--use-tv-api` or `--use-app-api`. |
| Mirror returns HTML (zip < 100KB) | Mirror down/rate-limited | Delete partial file; try next mirror. Install script in `install_tools.md` already loops. |

## Authentication

For full procedures see **`auth.md`**.

| Symptom | Cause | Recovery |
|---|---|---|
| BBDown: "字幕需要登录账号" | Member-only / restricted | `BBDown.exe login` (QR code), then re-run. |
| yt-dlp: "Sign in to confirm your age" | Age-restricted | Use cookies — see `auth.md`. |
| yt-dlp: "Sign in to confirm you're not a bot" | YouTube anti-bot for current IP; affects all unauthenticated paths including direct Innertube calls | Cookies required. Try `--cookies-from-browser firefox` if Firefox is installed; otherwise go straight to manual `cookies.txt` export (`auth.md` § Method 3). Switching `--extractor-args "youtube:player_client=..."` does **not** help once this error appears. |
| yt-dlp: "Could not copy Chrome cookie database" | Browser locking the SQLite db | Close browser fully (kill background `msedge.exe`/`chrome.exe` in Task Manager) and retry; or skip to manual cookies.txt (`auth.md` § Method 3). |
| yt-dlp: "Failed to decrypt with DPAPI" | Chromium ≥ v127 App-Bound Encryption (#10927) | `--cookies-from-browser` unrecoverable for that profile. Use manual cookies.txt (`auth.md` § Method 3). Firefox is unaffected. |

## Subtitle availability

| Symptom | Cause | Recovery |
|---|---|---|
| Empty subtitle list (only `danmaku` for B站) | Anonymous request limited | `BBDown.exe login`, then re-run. |
| Body is `[音乐]` / `[Music]` only | No real captions | Stop. Inform the user; suggest a Whisper-based ASR skill if available. |
| Auto exists but human doesn't (or vice versa) | Uploader's choice | Use whichever exists; `--write-auto-subs --write-subs` covers both. |
| Source language not in default `--sub-langs` | Language not requested | Re-run with `--sub-langs all`; pick the best result. **Always prefer the source language** — do not silently substitute a translated track. |
| BBDown reports zero AI subtitles | Forgot `--skip-ai false` | Re-read command; ensure `--skip-ai false` is present (default skips AI captions silently). |
| yt-dlp logs `Downloading subtitles:…` but writes no SRT/VTT; exits `Requested format is not available` | yt-dlp aborts the job before writing queued subtitles when no video format exists | Add **`--ignore-no-formats-error`**. Required whenever the page exposes only images / DRM streams. |
| yt-dlp writes `*.srv3` despite `--convert-subs srt` | Converter pipeline can't handle srv3 (typically ffmpeg missing) | Run `scripts/srv3_to_text.py <input.srv3> <out_basename>` for `.srt` + `.txt`. Stdlib-only. |
| yt-dlp writes `*.vtt` despite `--convert-subs srt`; stderr says `Preprocessing: ffmpeg not found` | SubtitlesConvertor needs ffmpeg to convert vtt→srt | Either install ffmpeg (`winget install Gyan.FFmpeg`) or write a small stdlib VTT→SRT script (strip `<00:00:00.000>` word-timing markers and `<c>...</c>` tags; for YouTube auto-captions, dedupe rolling lines by keeping each cue's last text line). |
| YouTube only offers translated auto-captions, no `*-orig` | Uploader did not provide a manual-language hint, so YouTube did not run source-language ASR | Translated tracks are second-hand machine translations — low quality. Use only as rough guide. When `<lang>-orig` exists, **always prefer it** over the same-language non-orig variant. |

## Encoding & display

| Symptom | Cause | Recovery |
|---|---|---|
| Chinese shows as `��������` in PowerShell | Console codepage GBK | `$env:PYTHONIOENCODING="utf-8"; chcp 65001` once per session. Always `Get-Content -Encoding UTF8`. Files on disk are still UTF-8 — only display is broken. |
| BBDown stdout garbled in `*> log.txt` | PowerShell pipe encoding | Same fix. SRT files are still UTF-8. |
| `srt_to_sentences.py` UnicodeDecodeError | Unusual BOM | Script already uses `utf-8-sig`; if still failing, verify it's really SRT (not VTT/binary) via `Get-Content "<file>.srt" -TotalCount 5`. |
| `srt_to_sentences.py` exit 2 | Empty / no-segments SRT | Stop; re-validate per SKILL.md Step 5 — SRT is invalid. |
| `fetch_metadata.py` exit 3, raw output contains `\ufffd` / mojibake | BBDown emits text in the host console code page (e.g. cp936 on zh-CN Windows); script is now multi-encoding aware (utf-8 → preferred → gbk/cp936/mbcs/cp1252) but very old script versions force UTF-8. | Update to current `fetch_metadata.py` (auto-detects encoding). If still failing, inspect raw bytes via `bbdown --only-show-info` redirected to a file and confirm the actual code page; fall back to manually authoring `metadata.json`. |
| `fetch_metadata.py` exit 3 | Upstream tool's output format changed | Manually inspect tool output; report to user — skill needs updating. |
| `rename_with_title.py` exit 2: `Unexpected UTF-8 BOM` | `metadata.json` was written with BOM (e.g. PowerShell `Out-File -Encoding utf8`) | Rewrite without BOM: `[System.IO.File]::WriteAllText($path, $json, [System.Text.UTF8Encoding]::new($false))`. Or hand-author with a tool that defaults to no-BOM UTF-8. |
