---
name: xerg
description: Find wasted AI spend in OpenClaw, Hermes, and Cursor.
homepage: https://xerg.ai
metadata:
  xerg:
    homepage: https://xerg.ai
    links:
      skill: https://xerg.ai/skill.md
      documentation: https://xerg.ai/docs
    primaryEnv: XERG_API_KEY
    requires:
      anyBins:
        - xerg
        - npx
      config:
        - ~/.xerg/config.json
        - ~/.config/xerg/credentials.json
        - ~/.xerg/remotes.json
    install:
      - kind: node
        package: "@xerg/cli"
        bins:
          - xerg
    envVars:
      - name: XERG_API_KEY
        required: false
        description: Optional Xerg Cloud workspace API key for explicit push, connect, and hosted MCP setup.
      - name: XERG_API_URL
        required: false
        description: Optional override for the Xerg API endpoint; defaults to https://api.xerg.ai.
    dependencies:
      - name: "@xerg/cli"
        type: npm
        url: https://www.npmjs.com/package/@xerg/cli
      - name: ssh
        type: other
        url: https://www.openssh.com/
      - name: rsync
        type: other
        url: https://rsync.samba.org/
      - name: railway
        type: npm
        repository: https://github.com/railwayapp/cli
---

# Xerg

Xerg is a local-first CLI for finding wasted AI spend in OpenClaw, Hermes, and Cursor. It audits dollars instead of raw token counts, separates confirmed waste from savings opportunities, and uses `--compare` to measure whether a workflow or model change actually helped.

## Quick Start

```bash
xerg init
xerg audit --compare
```

If `xerg` is not installed, use `npx @xerg/cli` with the same arguments.

## What It Audits

- OpenClaw gateway logs and session transcripts
- Hermes logs and session transcripts
- Cursor usage CSV exports via `xerg audit --cursor-usage-csv ./cursor-usage.csv`

## What It Finds

- Retry waste from failed calls before a later success
- Loop waste from runs that exceed efficient iteration bounds
- Context bloat from unusually large inputs
- Downgrade candidates where cheaper models may be enough
- Idle spend from recurring heartbeat or monitoring loops

## Optional Cloud

Local audits need no account. Hosted sync and hosted MCP are optional workspace features and only run when you explicitly use `xerg connect`, `xerg audit --push`, `xerg push`, or `xerg mcp-setup`.

## Links

- Docs: [xerg.ai/docs](https://xerg.ai/docs)
- Skill: [xerg.ai/skill.md](https://xerg.ai/skill.md)
- npm: [@xerg/cli](https://www.npmjs.com/package/@xerg/cli)
- Support: `query@xerg.ai`
