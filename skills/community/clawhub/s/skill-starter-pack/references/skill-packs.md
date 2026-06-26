# Skill Pack Details

## Pack Comparison

| Skill | Essential | Developer | Full | Downloads | Stars |
|---|:---:|:---:|:---:|---:|---:|
| agent-memory-architect | ✅ | ✅ | ✅ | — | — |
| self-improving | ✅ | ✅ | ✅ | 80k+ | ★ 414 |
| find-skills | ✅ | ✅ | ✅ | 228k+ | ★ 923 |
| quick-note | ✅ | ✅ | ✅ | — | — |
| weather | ✅ | ✅ | ✅ | 99k+ | ★ 298 |
| summarize | ✅ | ✅ | ✅ | 173k+ | ★ 657 |
| multi-search-engine | ✅ | ✅ | ✅ | 62k+ | ★ 316 |
| git-workflows | | ✅ | ✅ | — | — |
| browser-use | | ✅ | ✅ | — | — |
| image-analyzer | | ✅ | ✅ | — | — |
| github | | ✅ | ✅ | 116k+ | ★ 384 |
| agent-team-monitor | | | ✅ | — | — |
| decide | | | ✅ | — | — |
| proactive-agent | | | ✅ | 106k+ | ★ 565 |

**Total skills:** Essential 7 → Developer 11 → Full 14

## Skill Descriptions

### 🟢 Essential Pack

**agent-memory-architect** — by @ironmanc2014
Persistent, self-organizing memory for AI agents. Three-tier storage (HOT/WARM/COLD) with auto-learning from corrections, self-reflection, multi-agent memory sharing, and intelligent decay. Your agent remembers preferences, learns from mistakes, and gets smarter over time.

**self-improving** — by @ivangdavila
Self-reflection + Self-criticism + Self-learning + Self-organizing memory. After completing work, agent evaluates its own output, catches mistakes before you do, and permanently improves. Works across all platforms (Linux, macOS, Windows).

**find-skills** — by @JimLiuxinghai
The most downloaded skill on ClawHub (228k+). Say "how do I do X" or "find a skill for X" and the agent searches ClawHub, evaluates options, and installs the best match. Meta-skill that helps you discover all other skills.

**quick-note** — Quick capture for thoughts, ideas, and reminders. Say "记一下" (Chinese) or "note this" and the agent saves it instantly. No friction, no context switching.

**weather** — by @steipete
Current weather and forecasts for any location via wttr.in or Open-Meteo. No API key required. Simple and reliable.

**summarize** — by @steipete
Summarize anything: web pages, PDFs, images, audio files, YouTube videos. Uses the `summarize` CLI under the hood. Great for quickly digesting long content.

**multi-search-engine** — by @gpyAngyoujun
17 search engines in one skill — 8 Chinese (Baidu, Sogou, Zhihu, Bilibili, etc.) + 9 Global (Google, DuckDuckGo, WolframAlpha, etc.). Advanced operators, time filters, site-specific search. No API keys needed.

### 🔵 Developer Pack (additions)

**git-workflows** — Advanced git operations beyond add/commit/push. Interactive rebase, bisect for bug hunting, worktrees for parallel development, reflog recovery, subtrees/submodules management, merge conflict resolution, cherry-picking across branches, and monorepo workflows.

**browser-use** — Automate browser interactions for web testing, form filling, screenshots, and data extraction. Navigate websites, interact with page elements, fill forms, take screenshots, scrape data — all programmatically.

**image-analyzer** — Image recognition and analysis. Supports content identification, OCR text extraction, scene analysis, and object detection. Works with screenshots, photos, diagrams, and documents.

**github** — by @steipete
Full GitHub CLI integration via `gh`. Manage issues (`gh issue`), pull requests (`gh pr`), CI runs (`gh run`), and advanced API queries (`gh api`). Essential for any developer working with GitHub repos.

### 🟣 Full Pack (additions)

**agent-team-monitor** — Real-time monitoring dashboard for multi-agent teams. See what each agent is doing, how many tokens consumed, and overall progress. Essential when running parallel agent workloads.

**decide** — Auto-learns your decision patterns over time. Agent grows autonomy with earned trust, always confirms before assuming. Bridges the gap between "do everything I say" and "figure it out yourself."

**proactive-agent** — by @halthelobster
Transform your agent from a passive task-follower into a proactive partner that anticipates needs and continuously improves. Features WAL Protocol, Working Buffer, Autonomous Crons, and battle-tested patterns. Part of the popular Hal Stack.

## Requirements

- **OpenClaw** installed and running
- **clawhub** CLI: `npm i -g clawhub` or use via `npx clawhub`
- **Network** access to clawhub.ai
- **Optional per skill:**
  - `github` skill needs `gh` CLI installed and authenticated
  - `summarize` skill needs the `summarize` CLI
  - `browser-use` skill works best with a browser available on the host

## Troubleshooting

| Problem | Solution |
|---|---|
| `clawhub: command not found` | Run `npm i -g clawhub` |
| Rate limit exceeded | Wait 1-2 minutes and retry |
| Skill install fails | Try `clawhub install <name>` manually |
| Skills not showing after install | Restart your session or gateway |
