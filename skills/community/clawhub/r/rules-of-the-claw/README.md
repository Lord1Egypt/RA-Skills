# rules-of-the-claw

> A strong, field-tested Guardian baseline for OpenClaw Guardian.  
> 56 deterministic rules. No LLM overhead. Pure regex enforcement.

## What This Is

A ruleset for the [OpenClaw Guardian](https://github.com/fatcatMaoFei/openclaw-guardian) plugin. Guardian is the enforcement engine — this is the rulebook.

Rules block dangerous agent actions at the tool layer *before* they execute:

- **Credential theft** — blocks reads/exfil of `.env`, `.pem`, `.key`, `auth-profiles.json`, cloud credential paths, bot tokens
- **Data exfiltration** — blocks piping sensitive files to curl/wget/python/node, base64 encoding of secrets
- **Infrastructure destruction** — blocks `rm -rf` on critical dirs, DB drops/truncates, Docker container kills
- **Network scanning** — blocks nmap, masscan, nc port scanning
- **Git poisoning** — blocks pushes to unapproved remotes, archiving of sensitive paths

## Installation

### Via ClawHub (recommended)

```bash
clawhub install rules-of-the-claw
cd ~/.openclaw/workspace/skills/rules-of-the-claw
bash install.sh
```

### Manual

```bash
# Requires Guardian plugin already installed
cp rules-of-the-claw.json ~/.openclaw/extensions/guardian/guardian-rules.json
```

## Customize

Edit `~/.openclaw/extensions/guardian/guardian-rules.json`:

- Replace `YOUR_APP` with your app/project name (used in DB and Docker rules)
- Replace `YOUR_ORG` with your GitHub org (used in git remote rules)  
- Replace `YOUR_USER` with your username (used in approval messages)
- Set `"enabled": false` on any rule you don't need

## Rule Count

| Category | Rules |
|---|---|
| Credential protection | 27 |
| Environment & infrastructure | 14 |
| Network scanning | 3 |
| Git poisoning | 9 |
| Archive & transfer | 3 |
| **Total** | **56** |

## Links

- **GitHub:** <https://github.com/bahuleyandr/rules-of-the-claw>
- **Guardian plugin:** <https://github.com/fatcatMaoFei/openclaw-guardian>
- **ClawHub:** <https://clawhub.com/skills/rules-of-the-claw>

## License

MIT
