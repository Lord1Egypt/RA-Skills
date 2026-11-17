# psyseal-scan

The free Psyseal scanner. MIT-0.

It reviews the AI agents on your computer (OpenClaw, Hermes Agent, nanobot, PicoClaw, ZeroClaw, NanoClaw or any agent folder) and tells you what loads on every message, what heartbeats and scheduled tasks cost, which plaintext secrets are sitting in memory or skills, and which memory looks planted or bloated. Every finding comes with a concrete fix.

It runs on your computer, reads files only, uses no network and has no dependencies. Needs Node.js 20 or newer.

## Run it

```bash
npx psyseal-scan --lang en
```

Or from a copy of this repository: `node scripts/psyseal-scan.mjs --lang en`. See `--help` for all options (`--path <folder>` checks any agent folder).

## As an agent skill

- OpenClaw (from ClawHub): `openclaw skills install @psyseal/psyseal-scan`
- Claude Code, Cursor, Codex, Gemini CLI and other agents (skills CLI): `npx skills add psyseal/psyseal-scan`

## As an MCP server

The same scan as one read-only tool, `scan_agents`, over stdio:

```json
{
  "mcpServers": {
    "psyseal-scan": { "command": "npx", "args": ["-y", "psyseal-scan", "mcp"] }
  }
}
```

Claude Code: `claude mcp add psyseal-scan -- npx -y psyseal-scan mcp`

Name in the official MCP Registry: `io.github.psyseal/psyseal-scan`.

## What it never does

It never sends anything over the network, writes or deletes files, starts other programs or follows symlinks. The report shows the type, file and line of each secret, never its value, and never quotes memory text.

This repository holds only the free scanner. The full Psyseal package, including the paid cleanup and the signed seal, is at https://github.com/psyseal/scanner, and the service at https://psyseal.com. The report ends with one line about it; `--no-cta` removes it.

---

**Español:** el escáner gratis de Psyseal (MIT-0). Revisa en tu computadora cuánto te cuestan los latidos y tareas programadas de tu agente, qué claves quedaron expuestas y qué memoria está inflada o trae instrucciones plantadas. No usa la red ni tiene dependencias. Córrelo con `npx psyseal-scan --lang es`. También funciona como skill y como servidor MCP (`npx -y psyseal-scan mcp`). Más información en https://psyseal.com.
