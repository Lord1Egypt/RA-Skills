# Authentication & Cookies Guide

When and how to authenticate against Bilibili / YouTube. Read this only when you encounter an auth error — most public videos serve subtitles without login.

---

## When you need authentication

| Scenario | Platform | Symptom |
|---|---|---|
| Member-only / 大会员专享 | Bilibili | "需要登录" / "大会员专享" |
| Region-locked | Both | HTTP 403 / "video unavailable in your region" |
| Age-restricted | YouTube | "Sign in to confirm your age" |
| Anti-bot triggered | YouTube | "Sign in to confirm you're not a bot" |
| Premium / members-only | YouTube | "members only" |
| Edited / private listing | Both | 404 or empty subtitle list |

---

## Method 1: BBDown QR-code login (Bilibili)

Cleanest path for Bilibili. No browser dependency.

```powershell
BBDown.exe login
```

Prints a QR code; scan with the Bilibili mobile app. Token saved as `BBDown.data` in BBDown's working directory and persists across runs. Verify:

```powershell
BBDown.exe "<URL>" --only-show-info
# Look for: 检测账号登录... 登录用户名: <your-name>
```

To log out: delete `BBDown.data`.

---

## Method 2: Export cookies.txt manually (recommended; works for both platforms)

> **YouTube 认证首选方案。** `--cookies-from-browser` 在现代 Chromium 上频繁失败（见下方 Method 3 说明），直接导出 cookies.txt 更快更稳。

Most reliable. Does not require closing the browser. Unaffected by App-Bound Encryption.

**Steps (using "Get cookies.txt LOCALLY"):**

1. **Install the extension** — open-source, audited, fully-local. No telemetry.
   - Chrome / Edge: https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
   - Firefox: search "cookies.txt" on https://addons.mozilla.org/ and pick the open-source one (verify the source repo on GitHub before installing — multiple similarly-named extensions exist).

2. **Open the target page** *while logged in*. For YouTube, navigate to the specific video URL. For Bilibili, open `bilibili.com`.

3. **Export.** Click the extension's toolbar icon (pin from the puzzle-piece menu first if needed) → **Export**. Saves `www.youtube.com_cookies.txt` (or similar) to Downloads.

4. **Note the file path.** Typically `%USERPROFILE%\Downloads\www.youtube.com_cookies.txt` on Windows, `~/Downloads/cookies.txt` on POSIX. Tell the agent the path explicitly.

5. **Pass to the tool.**

```powershell
# Windows
yt-dlp --cookies "C:\Users\<you>\Downloads\www.youtube.com_cookies.txt" `
       --write-auto-subs --sub-langs "<lang>" --skip-download "<URL>"

# Bilibili (BBDown takes a single-line cookie STRING, not a file path):
BBDown.exe "<URL>" --cookie "<one-line-cookie-string>"
```

```bash
# POSIX
yt-dlp --cookies "/path/to/cookies.txt" --write-auto-subs --sub-langs "<lang>" --skip-download "<URL>"
```

For BBDown's `--cookie`, extract `SESSDATA=...; bili_jct=...; DedeUserID=...` from the exported file and concatenate into a single line separated by `; `.

**Cookie file lifetime.** Stays valid as long as the browser session remains logged in (typically weeks to months). Re-export only when auth errors return. Storing under `<TOOLS_DIR>/cookies/<site>.txt` makes it reusable.

---

## Method 3: yt-dlp `--cookies-from-browser` (YouTube) — limited reliability on modern Chromium

> ⚠️ 此方法在现代 Chromium 上经常失败，**优先使用 Method 2（cookies.txt）**。

```powershell
# Replace <lang> with the source language code from --list-subs
yt-dlp --cookies-from-browser edge --write-auto-subs --sub-langs "<lang>" --skip-download "<URL>"
```

Supported browsers: `chrome`, `chromium`, `edge`, `firefox`, `brave`, `opera`, `vivaldi`, `safari` (macOS).

**⚠️ Frequently fails on modern Chromium.** Two failure modes — only the first is recoverable:

| Failure | Symptom | Recoverable? |
|---|---|---|
| Cookie DB locked by running browser | `ERROR: Could not copy Chrome cookie database` (issue #7271) | Yes — fully close the browser (kill all background `msedge.exe`/`chrome.exe` in Task Manager, including processes from "let Edge run in background apps"), then retry. |
| App-Bound Encryption (Chromium ≥ v127) | `ERROR: Failed to decrypt with DPAPI` (issue #10927) | **No** — Chromium added a DPAPI encryption layer yt-dlp cannot decrypt even when the browser is closed. **Switch to Method 2.** |

Firefox is unaffected by App-Bound Encryption, so `--cookies-from-browser firefox` may still work.

---

## Security reminder

Cookie files contain your active session. Treat them like passwords:

- Store in a controlled location (`<WORK_DIR>` for one-off, `<TOOLS_DIR>` for reuse) — never commit to git
- Add `cookies.txt` to `.gitignore` if working in a tracked repo
- Delete after one-off tasks
- Never paste cookie content into chat or share with third parties
