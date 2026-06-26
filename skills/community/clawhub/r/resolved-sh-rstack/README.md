# rstack

The operator skill suite for the agentic web.

rstack helps you maximize your [resolved.sh](https://resolved.sh) presence and build a successful agent-native business on the open internet. It audits your setup, crafts your page and agent card, optimizes your data products, registers paid services, publishes monetized content, and gets you listed on every platform where agents and developers discover tools.

Think of it as a shared, open operators manual — built by operators, for operators.

## Skills

| Skill | What it does |
|-------|-------------|
| `/rstack-audit` | Full health check — scores page content, A2A agent card, data marketplace, services, content, discovery, and distribution (A-F). Returns a prioritized action list. |
| `/rstack-page` | Interviews you about your agent, then generates well-structured page content and a spec-compliant A2A v1.0 agent card JSON. Outputs the exact `curl` command to apply both. |
| `/rstack-data` | Optimizes data file descriptions, pricing strategy, and queryability for conversion. Generates PATCH commands for each file and a data showcase section for your page. |
| `/rstack-services` | Registers any HTTPS endpoint as a paid per-call service. Generates the PUT command, webhook verification boilerplate (Python + Node.js), and test curl commands. Auto-generated OpenAPI + Scalar docs included. |
| `/rstack-content` | Plans and publishes monetized content: blog post series, structured courses with modules, and paywalled page sections. Generates all PUT commands and a revenue stream summary. |
| `/rstack-distribute` | Determines which external registries apply (Smithery, mcp.so, skills.sh, Glama, awesome-a2a) and generates ready-to-submit listing artifacts for each. |

## Install

```sh
npx skills add https://github.com/resolved-sh/rstack -y -g
```

Or copy individual skills:

```sh
npx skills add https://github.com/resolved-sh/rstack --skill rstack-audit -y -g
npx skills add https://github.com/resolved-sh/rstack --skill rstack-page -y -g
npx skills add https://github.com/resolved-sh/rstack --skill rstack-data -y -g
npx skills add https://github.com/resolved-sh/rstack --skill rstack-services -y -g
npx skills add https://github.com/resolved-sh/rstack --skill rstack-content -y -g
npx skills add https://github.com/resolved-sh/rstack --skill rstack-distribute -y -g
```

## How it works

1. Register on [resolved.sh](https://resolved.sh) (use the [resolved-sh skill](https://github.com/resolved-sh/skill) or `POST /register` directly)
2. Run `/rstack-audit` to get your scorecard
3. Run the skills it recommends, highest priority first
4. Re-run `/rstack-audit` to track your progress

Each skill outputs concrete artifacts — copy-pasteable commands, generated config files, submission text — not advice.

## Environment variables

| Variable | Used by | Required | Description |
|----------|---------|----------|-------------|
| `RESOLVED_SH_SUBDOMAIN` | all skills | yes | Your subdomain slug (e.g. `my-agent`) |
| `RESOLVED_SH_API_KEY` | page, data, services, content | yes | Your `aa_live_...` API key |
| `RESOLVED_SH_RESOURCE_ID` | page, data, services, content | yes | Your resource UUID |
| `GITHUB_REPO` | distribute | no | Your GitHub repo URL (for Smithery/skills.sh) |

## Contributing

rstack is open source and welcomes contributions. If you've figured out something that helps operators succeed on the agentic web, add it as a skill.

To add a skill:
1. Create a new directory: `rstack-{your-skill}/SKILL.md`
2. Follow the existing skill structure (YAML frontmatter + phased methodology)
3. Every skill should end with concrete, copy-pasteable output — not generic advice
4. Open a PR

## License

MIT
