# skillguard-check

A drop-in **AI Skill** that audits the skills installed on this machine
against [skillguard.vip](https://skillguard.vip)'s public security database.
When invoked by an agent (Claude Code, OpenClaw, MCP-aware client, …), it
discovers locally-installed skills, queries each one, and returns a
machine-readable report of **blocked** and **high-risk** entries.

## Why

ClawHub and other AI Skill marketplaces let anyone publish a skill bundle.
We've audited the public catalog ([report](https://skillguard.vip/report/clawhub)):
**1.78% of skills auto-blocked** for `curl|sh`, hard-coded private keys,
Chrome credential reads, and similar patterns. This skill lets agents flag
those for the user *before* they invoke them.

## Install

### Claude Code

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/yangyixxxx/skillguard.git skillguard-check-tmp
cd skillguard-check-tmp
git sparse-checkout set skills/skillguard-check
mv skills/skillguard-check ../skillguard-check
cd .. && rm -rf skillguard-check-tmp
```

Or just copy the files directly:

```bash
mkdir -p ~/.claude/skills/skillguard-check/scripts
curl -fsSLo ~/.claude/skills/skillguard-check/SKILL.md \
  https://raw.githubusercontent.com/yangyixxxx/skillguard/main/skills/skillguard-check/SKILL.md
curl -fsSLo ~/.claude/skills/skillguard-check/scripts/check.py \
  https://raw.githubusercontent.com/yangyixxxx/skillguard/main/skills/skillguard-check/scripts/check.py
```

### OpenClaw / others

Same idea — drop the directory under whatever path your agent reads skills
from (`~/.openclaw/skills/`, `~/.local/share/claude-skills/`, etc.).

## Usage

The agent invokes it automatically when relevant ("are my skills safe?").
You can also run it standalone:

```bash
python3 ~/.claude/skills/skillguard-check/scripts/check.py --pretty
```

Sample output:

```json
{
  "total": 12,
  "audited": 9,
  "blocked": [
    {
      "slug": "openclaw-omni-expert",
      "path": "/Users/x/.claude/skills/openclaw-omni-expert",
      "score": 3,
      "riskLevel": "Critical",
      "findingsCount": 155,
      "auditUrl": "https://skillguard.vip/skills/clawhub/openclaw-omni-expert"
    }
  ],
  "highRisk": [],
  "medium": [],
  "safe": 8,
  "unaudited": [
    { "slug": "my-private-skill", "reason": "not in skill-guard database" }
  ]
}
```

Exit code: `0` if no blocked / high-risk skills, `1` if any found.

## Flags

| flag | default | meaning |
|---|---|---|
| `--api <url>` | `https://skillguard.vip` | API base — point at a self-hosted skill-guard if you run one |
| `--extra-path <dir>` | (none) | Add a discovery path. Repeatable. |
| `--slug <name>` | (none) | Check just one slug, skip discovery. Repeatable. |
| `--concurrency <n>` | 8 | Parallel HTTP requests |
| `--pretty` | off | Pretty-print the JSON |

## Privacy

- The script reads only directory **names** under the skill paths, not file
  contents. Your skills' source code never leaves the machine.
- Each name (slug) is sent as a path component to skillguard.vip in a plain
  HTTPS GET. No headers identify the user; standard Cloudflare access logs
  apply.
- No telemetry, no analytics, no user identifier.

## Source

- This skill: <https://github.com/yangyixxxx/skillguard/tree/main/skills/skillguard-check>
- skill-guard scanner: <https://github.com/yangyixxxx/skillguard>
- Public audit DB: <https://skillguard.vip/skills>
- ClawHub audit report: <https://skillguard.vip/report/clawhub>

Apache-2.0.
