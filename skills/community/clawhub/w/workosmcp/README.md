# WorkOS for OpenClaw

A ClawHub skill that teaches OpenClaw and other MCP-compatible agents how to
use **WorkOS** — a self-hosted workspace platform with documents, databases,
tasks, meeting transcription, and sharing.

WorkOS exposes its full data model through a remote MCP server at
`https://workos.no/api/mcp` with OAuth 2.1. This skill gives the agent:

- Clear rules for **when** to use WorkOS.
- An overview of the ~60 tools available, grouped by area.
- Connection recipes for OpenClaw, Claude Desktop, Cursor, Cline, and OpenCode.
- Workflow patterns and troubleshooting.

## Contents

```
workos-clawhub-skill-en/
├── SKILL.md             # Main agent-facing instructions
├── README.md            # This file
├── LICENSE              # MIT-0
├── docs/
│   ├── connect.md       # Per-client connection setup
│   ├── tools.md         # Full tool catalog
│   └── workflows.md     # Example flows
└── examples/
    └── prompts.md       # Sample prompts for testing
```

## License

MIT-0 — free use, no attribution required. See `LICENSE`.

## Maintenance

- Homepage: <https://workos.no>
- For agents: <https://workos.no/for-agenter>
- Issues / contact: hakon@skjldlabs.com
