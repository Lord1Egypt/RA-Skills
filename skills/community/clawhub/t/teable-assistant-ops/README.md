# Teable Assistant Skill

[Teable](https://teable.ai) is an AI spreadsheet for business. This skill helps AI assistants operate Teable projects, tables, fields, views, records, SQL queries, automations, routines, apps, and generated media through the Teable CLI.

## Install from the official source

```sh
npx skills add https://github.com/teableio/agent-skills --skill teable-assistant-ops
```

Follow SKILL.md and guides/cli-install.md to install the Teable CLI and authenticate. Node.js 18 or newer is required by the installation script. Skill metadata specifies Teable CLI >=0.6.45. A Teable account or an appropriately configured Teable instance is required for data operations.

- Website: https://teable.ai
- Setup: https://help.teable.ai/en/basic/ai/teable-skill
- Source: https://github.com/teableio/agent-skills/tree/main/skills/teable-assistant-ops
- Source commit: f9a9ecaeb46d21b03416f43ac567841e11079b51
- Skill version: 1.10.0
- License: MIT (see LICENSE)

This distribution preserves the upstream skill files unchanged and adds this README plus the repository's license. Review the skill and scripts before use. The install script installs or upgrades @teable/cli and starts browser authentication if needed.
