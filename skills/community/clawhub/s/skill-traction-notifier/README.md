# skill-surge-notifier

Monitors [ClawHub](https://clawhub.ai/skills) for skills gaining traction. Tracks downloads and stars over time, detects surges, and always shows you what's moving — so your agent stays ahead of the curve.

Works with any OpenClaw agent, nanobot, or AI framework with shell access. Drop the `SKILL.md` into your agent and it handles the rest.

## Usage

```bash
node {baseDir}/cli.js check    # top movers + surge alerts
node {baseDir}/cli.js fetch    # live top 20 by downloads
node {baseDir}/cli.js status   # last check, config summary
```

## Example output

```
Top 5 movers since last check:

  1. API Gateway                         +1,842 DL  (+5.1%)
  2. Memoclaw Skill                        +312 DL  (+21.1%)
  3. Vincent - Wallet                      +201 DL  (+4.1%)
  4. Kubernetes                            +180 DL  (+3.7%)
  5. Whatsapp Ultimate                      +98 DL  (+3.6%)

3 surge(s) — 1 matches your profile

 SURGE: Memoclaw Skill
   Memory-as-a-Service for AI agents. Store and recall memories...
   Relevance: ████░ 8/10  [memory, agents]
   Downloads: 1,504 (+21.1%)  |  Stars: 4
   Why: +21.1% download growth
   Install: clawhub install memoclaw
```

## Relevance scoring

Set a profile once and surges get ranked by how relevant they are to your agent:

```bash
skill-surge-notifier profile set "research assistant focused on web search and summarization" "search,summarize,web,research"
```

Surges are scored 0-10 and sorted — most relevant first. No server, no account, stored locally in `~/.skill-surge-notifier/`.

## All commands

| Command | What it does |
|---|---|
| `check` | Run surge detection, show top movers, update state |
| `fetch` | Show top 20 skills by downloads |
| `status` | Last check time, top 5, current config |
| `profile` | Show current profile |
| `profile set "desc" "kw1,kw2"` | Set profile for relevance scoring |
| `config movers=5` | Number of top movers to show |
| `config movers-off` | Disable top movers |
| `config growth=30` | Min growth % to trigger surge alert |
| `config downloads=50000` | Min downloads to trigger surge alert |
| `config stars=200` | Min stars to trigger surge alert |

## Scheduling

Run automatically every 4 hours via cron:

```bash
0 */4 * * * node {baseDir}/cli.js check >> ~/.skill-surge-notifier/surge.log 2>&1
```

Or let your agent schedule it via its heartbeat.

## For agents

Drop `SKILL.md` into your agent's context. It will run checks on a schedule — reporting surges directly in chat. To enable relevance scoring, run `node {baseDir}/cli.js profile set` with your agent's description and keywords.

---

Built by [@gkauf_gm](https://x.com/gkauf_gm)
