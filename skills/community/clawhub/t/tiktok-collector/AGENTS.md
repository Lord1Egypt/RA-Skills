# TikTok Collector (MonsterGet)

Collect TikTok data (video search, creator search, hashtag search, creator videos, creator profiles) as CSV, driven by an AI agent, scraped through the user's real logged-in browser via the MonsterGet browser extension (anti-ban). Works in any AI client that can run shell commands.

## Language rule

Always reply to the user in the user's own language (zh → 中文, ja → 日本語, es → Español, …).

## ⚠️ Answering "how to use" questions — user-first rule

When the user asks "怎么使用", "how to use this skill", "怎么用爬虫", or anything equivalent asking for usage guidance:

**The user is an end user, not a developer of this skill. Never show them bash commands, script paths (`run-scrape.sh`, `choose-browser.sh`), API endpoints (`monsterget.com/api/…`), taskIds, polling logic, VERSION.json, state.json, or any implementation detail.**

Instead, reply with 4-8 lines of conversational text in the user's language, giving 2-3 example natural-language prompts they can just say:

> 你可以直接对我这样说：
>
> - "抓取 TikTok 上关于 **mike tyson** 的视频 50 条"
> - "搜索做 **beauty** 内容的创作者 30 个"
> - "抓取 **#kpop** 标签下的视频"
> - "导出 **@tiktok** 这个账号的全部视频"
>
> 我会自动帮你抓取并生成 CSV 文件。需要什么直接说就行。

The implementation details (bash commands, script names, API URLs, polling) are for your execution only — they must never appear in your answer to the user.

## When to use

The user asks for TikTok data: videos about X, creators doing X, videos under #tag, all videos by @creator, or creator profile stats — for research, marketing, or content monitoring.

## How it works

```
AI generates taskId ──▶ opens browser URL ──▶ page creates task, extension scrapes ──▶ AI polls status ──▶ AI downloads CSV
```

No server-side TikTok scraping. The scrape runs inside the user's real TikTok session (logged in, with the MonsterGet extension). That's what keeps accounts safe from bans.

## First-run flow (pure manual — no code verification)

The user needs 3 things, all in the **same browser** (the one they chose). The AI shows the guide and the user confirms manually. **No script checks anything.**

**a. Show the full 3-step guide with links** (in the user's language) — so the user knows exactly what to prepare:

> 用这个 skill 前需要准备 3 件事（都用同一个浏览器：**Edge 或 Chrome**）：
> ① 安装 MonsterGet 扩展 → 打开 https://monsterget.com/install 安装
> ② 登录 monsterget.com → 打开 https://monsterget.com 注册并登录
> ③ 登录 TikTok → 打开 https://www.tiktok.com 登录你的账号
>
> 装好扩展后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"），全部准备好了回复"好了"。

**b. WAIT** for the user to reply with the browser name and "好了". **Never run any detection script, never scan the disk, never verify programmatically.** The user's manual confirmation is the only check.

**c. Save the browser choice** — whatever the user said, save it directly:

```bash
bash ~/.monsterget/skill/scripts/choose-browser.sh edge
# (or chrome — user said Chrome)
# → {"ok":true,"browser":"edge",...}
```

The choice persists across sessions. Never second-guess it with a disk scan.

**d. Confirm + offer example prompts:**

> ✅ 都准备好了，可以开始抓取了！
> 试试下面任意一句：
> - 抓取关于 "mike tyson" 的 TikTok 视频 50 条
> - 找出做 "beauty" 内容的 TikTok 创作者 30 个
> - 抓取 #kpop 标签下的视频 30 条
> - 抓取 @tiktok 这位创作者的全部视频
> - 抓取 @mike、@jenifer、@tiktok 的主页数据

If anything is missing later (scrape fails), use the failure checklist in SKILL.md — again, manual only, never a script check.

## Scripts

All scripts live at `~/.monsterget/skill/scripts/`. Resolve once at the start of the session and **exit immediately if not found** — don't proceed without them.

```bash
SCRIPTS="$HOME/.monsterget/skill/scripts"
if [ ! -d "$SCRIPTS" ]; then
  echo "Skill not installed — run the install instruction first." >&2
  exit 1
fi
```

Each script prints one JSON object to stdout and exits 0 on success / 1 on failure.

| Script | Purpose |
|--------|---------|
| `update-skill.sh` | Session start — auto-update check. Compare local version against GitHub, auto-download updates. |
| `choose-browser.sh <edge\|chrome>` | Save the user's browser choice (manual — no verification, saves whatever the user says). |
| `run-scrape.sh <pagePath> <param> <value> [count]` | Full scrape: generate taskId, open browser, verify process, poll, download CSV. |
| `set-download-dir.sh [<dir>]` | Choose where scraped CSVs are saved (persists in state). No arg = system Downloads. Ask the user once per machine. |

> **🚫 Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`** — archived reference only. The user guarantees all conditions manually. The AI must not call them during installation, before a scrape, or on failure.

### Browser choice

During installation the user verbally confirms which browser has the MonsterGet extension; the AI saves it with `choose-browser.sh`. `run-scrape.sh` reads the saved `browser_pref` and opens that browser. No detection, no scanning, no second-guessing.

### Scrape

```bash
bash ~/.monsterget/skill/scripts/run-scrape.sh <pagePath> <param> <value> [count]
```

| Intent | `pagePath` | `param` | `value` example |
|--------|-----------|---------|----------------|
| videos about X | `/tiktok-search-video` | `query` | `mike tyson` |
| creators doing X | `/tiktok-search-user` | `query` | `beauty` |
| videos under #tag | `/tiktok-tag` | `query` | `kpop` (no `#`) |
| videos by @creator | `/tiktok-user-videos` | `username` | `@mike` |
| profile of @creator | `/tiktok-profile` | `username` | `@mike` |
| several profiles | `/tiktok-profile` | `usernames` | `mike,jenifer,tiktok` |

Default counts: video search 50, creator search 30, tag 30, user videos 50. Max: 300.

The script generates the taskId, opens the browser (fire-and-forget), verifies the process started, polls until ready (up to 5 minutes), and downloads the CSV. It never waits for the user.

Output on success: `{"status":"ready","taskId":"...","file":"...csv","rowCount":N,"url":"..."}`

## Behavior rules for the agent

- **Open + verify + poll in one shot.** Never ask "is the browser open?" or "shall I continue?".
- **Multiple scrapes = orchestrate them one at a time.** Run the first `run-scrape.sh`, wait for its result, then run the next. The page's `auto=1` flow already inserts a random 5-10s delay before the scraper window opens (anti-detection), so you don't add any sleep — just run each scrape and report between them.
- **Show the CSV path + a few rows** so the user trusts the result.
- **First scrape each session**: tell the user once that this drives their real TikTok account (user's account, user's responsibility).
- **Where CSVs are saved**: the first time you scrape, ask the user where CSV files should go — "保存到系统下载目录（默认）可以吗？还是换个路径？" Then save their choice with `set-download-dir.sh` (no arg = system Downloads, or pass a path). It persists, so ask at most once per machine; `run-scrape.sh` reports the `dir` in its output.
- **On failure**: use the error field to explain exactly what to fix — don't just say "try again".
- **Pre-task reminder**: before every scrape, read `~/.monsterget/state.json` and say the reminder sentence from SKILL.md — this is the user's only confirmation that the browser is about to open. Never skip it.

## Common errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `not_found` / `timeout` | Extension missing, not logged in, or the tab was closed | Run the 3-point manual checklist (SKILL.md Step 3) — the user checks each in the browser by hand |
| `platform_reachable: false` | monsterget.com unreachable | Ask user to check the URL manually |
| `browser did not start` | Launch command failed | Ask user to open the URL manually in the extension browser |
| Not ready in 5 minutes | Extension missing / not logged in / tab closed | Keep the tab open until the scrape finishes |
| `already_downloaded` | CSV already fetched | Run again (new taskId) |
| `429 too_many_concurrent_scrapes` | Free tier has 1 slot | Wait for running task to finish, then retry |
