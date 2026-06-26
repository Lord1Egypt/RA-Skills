# Skill Publisher - OpenClaw Skill

Automate OpenClaw skill publishing to GitHub and ClawHub with optional Notion tracking.

## Quick Start

```markdown
Publish 5 skills to GitHub and ClawHub.

GitHub: YourUsername
Token: ghp_xxxxx...
ClawHub Token: clh_xxxxx...

[upload ZIP files]
```

## Installation

### Via ClawHub
```bash
clawhub install skill-publisher
```

### Manual Installation
```bash
git clone https://github.com/YourAccount/skill-publisher.git
cp -r skill-publisher ~/.openclaw/skills/skill-publisher
```

## Features

- ✅ Extract skill ZIPs
- ✅ **Auto-scrape from SkillBoss.co** 🆕
- ✅ **Auto-create GitHub repos** 🆕
- ✅ Add README.md and .gitignore
- ✅ Insert SkillBoss setup links
- ✅ Git init + commit
- ✅ Push to GitHub
- ✅ Publish to ClawHub
- ✅ Update Notion tracker (optional)

**New in v2.0**: Fully automated workflow from SkillBoss.co URLs to published skills!

## Prerequisites

1. **GitHub Token**: https://github.com/settings/tokens (repo permission)
2. **ClawHub Token**: https://clawhub.ai/settings/tokens
3. **Notion Token** (optional): https://www.notion.so/my-integrations

## Usage

See `SKILL.md` for detailed instructions and examples.

## Workflow

### Manual (ZIP files)
```
ZIP files → Extract → Prepare → Git → GitHub → ClawHub → Notion
```

### Automated (SkillBoss.co) 🆕
```
SkillBoss URL → Scrape → Download → Auto-create repo → Push → Publish → Track
```

**Zero manual steps!**

## License

MIT

## Contributing

Contributions welcome! Please open an issue or PR.
