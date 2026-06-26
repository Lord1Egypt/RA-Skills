# skill-auditor-in-sandbox

A [Claude Code](https://claude.ai/claude-code) skill that launches a [NovitaClaw](https://novita.ai/docs/guides/novitaclaw) (OpenClaw) sandbox, installs a specified skill, and generates an installation & security audit report.

Test community skills in an isolated environment before installing them locally.

## Installation

### Via ClawHub

```bash
clawhub install freecodewu/skill-auditor-in-sandbox
```

### Via GitHub

```bash
git clone https://github.com/freecodewu/skill-auditor-in-sandbox.git
cd skill-auditor-in-sandbox
npm install
```

Then copy the skill file into your project:

```bash
cp skill-auditor-in-sandbox.md /path/to/project/.claude/skills/
cp -r scripts/ /path/to/project/scripts/
```

## Prerequisites

- **Node.js** >= 18.0.0
- **NOVITA_API_KEY** — get one from [Novita AI Key Management](https://novita.ai/settings/key-management)
- **novitaclaw CLI** — install with:
  ```bash
  curl -fsSL https://novitaclaw.novita.ai/install.sh | bash
  ```

## Usage

```
/skill-auditor-in-sandbox <skill-name>
```

Example:

```
/skill-auditor-in-sandbox pskoett/self-improving-agent
```

### What it does

1. Launches a NovitaClaw sandbox
2. Installs the skill (tries ClawHub -> GitHub -> clawhub.ai git clone)
3. Runs a security audit scanning for suspicious patterns, network calls, external paths, and dependencies
4. Generates a structured report with risk level (LOW / MEDIUM / HIGH / CRITICAL)
5. Offers sandbox lifecycle management (keep / pause / stop)

### Scripts (standalone usage)

```bash
# Install a skill into a sandbox
SANDBOX_ID=<id> NOVITA_API_KEY=<key> SKILL_NAME=pskoett/self-improving-agent node scripts/install-skill.mjs

# Audit an installed skill
SANDBOX_ID=<id> NOVITA_API_KEY=<key> SKILL_NAME=pskoett/self-improving-agent node scripts/audit-skill.mjs
```

Both scripts output JSON to stdout.

## Project Structure

```
skill-auditor-in-sandbox/
├── skill-auditor-in-sandbox.md    # Skill definition (dispatcher + report template)
├── scripts/
│   ├── install-skill.mjs          # Sandbox skill installation with 3-tier fallback
│   └── audit-skill.mjs            # Security pattern scanner
├── package.json
├── .gitignore
├── README.md
└── LICENSE
```

## License

MIT
