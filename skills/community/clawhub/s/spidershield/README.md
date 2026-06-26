# SpiderShield — OpenClaw Security Skill

Security scanning and trust scoring for OpenClaw skills.
4,000+ skills pre-scanned. 93.6% precision. 0.1s trust score lookup.

## Install via ClawHub

```bash
npx clawhub install spidershield
```

`/spidershield check` works immediately — no extra setup needed.

For local scanning commands (scan, audit-config, fix, pin, scan-all), also install:
```bash
pip install spidershield
```

## Commands

| Command | Description |
|---------|-------------|
| `/spidershield check <author/skill>` | Trust score lookup (0.1s, pre-computed) |
| `/spidershield scan <path>` | Skill malware scan (24 detection rules) |
| `/spidershield audit-config` | OpenClaw config security audit |
| `/spidershield fix` | Auto-fix insecure config settings |
| `/spidershield pin add\|verify\|list` | Rug pull detection (content hash pinning) |
| `/spidershield scan-all` | Scan all installed skills |

## Privacy

- `/check` sends only author/skill slug to API
- All other commands run **entirely locally** — no data leaves your machine

## Source

- [SKILL.md](SKILL.md) — full command documentation
- [SpiderRating](https://spiderrating.com) — Trust Registry
- [GitHub](https://github.com/teehooai/spidershield)
