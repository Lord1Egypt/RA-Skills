<p align="center">
  <h1 align="center">ucli</h1>
  <p align="center">
    The serious CLI for serious Unraid operators.<br>
    Built on the Unraid 7.2+ GraphQL API. Designed for humans and agents.
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/TypeScript-5.6%2B-blue?logo=typescript&logoColor=white" alt="TypeScript 5.6+">
    <img src="https://img.shields.io/badge/Unraid-7.2%2B-orange?logo=unraid&logoColor=white" alt="Unraid 7.2+">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
    <img src="https://img.shields.io/badge/AI_agent-ready-blueviolet" alt="AI Agent Ready">
  </p>
</p>

---

## Why this exists

The WebUI is slow for repetitive work. SSH alone is too raw. Agents need structured output that doesn't fight back.

ucli wraps the Unraid GraphQL API into a stateless CLI with `json`, `yaml`, `table`, and human-readable output. No REPL, no interactive shell state, no surprises in automation.

## Quick start

### npm

```bash
npm install -g unraid-cli
```

### From source

```bash
git clone https://github.com/ingodibella/unraid-cli.git
cd unraid-cli
npm install
npm run build
npm link
```

Then point it at your server:

```bash
ucli --host http://192.168.1.10:7777 --api-key YOUR_API_KEY system info
```

Or set up a config profile:

<details>
<summary>Config file setup</summary>

Create `~/.config/ucli/config.yaml`:

```yaml
default_profile: lab
profiles:
  lab:
    host: http://192.168.1.10:7777
    apiKey: YOUR_API_KEY
    output: table
    timeout: 30
```

Then just:

```bash
ucli system info
ucli containers list --output json --filter state=RUNNING
```

</details>

## For AI agents

> **TL;DR:** Pass `--output json --quiet`, point at `AGENTS.md` for workflows and safety rules.

```bash
ucli --output json --quiet system info
ucli containers list --output json --fields id,names,state,status --sort names:asc
ucli notifications latest --output json --quiet
```

`--fields` cuts token waste. `--filter` and `--sort` move data shaping into the CLI. Stateless commands make retries safe. Clean stderr and explicit exit codes make failure handling predictable.

See `AGENTS.md` for recommended workflows, guardrails, and anti-patterns.

## Features

| | |
|---|---|
| GraphQL API | Built on the official Unraid 7.2+ API |
| Output formats | `json`, `yaml`, `table`, human-readable |
| Agent-first shaping | `--fields`, `--filter`, `--sort` baked in |
| Stateless | No REPL, no session state, safe for scripts and cron |
| Non-interactive | Pipes cleanly, no hanging prompts |
| Strong types | Schema-driven TypeScript from GraphQL operations |
| Retry logic | Configurable `--timeout` and `--retry` |

## Commands

15 command groups covering the full Unraid surface:

| Group | What it does |
|---|---|
| `system` | Info, health, status, resources, uptime |
| `array` | State, devices, parity, parity-check control |
| `disks` | Inventory, SMART, temperature, usage, mount actions |
| `containers` | List, inspect, logs, stats, start/stop/restart/pause/remove |
| `notifications` | List, latest, get, create, archive, unread ops |
| `vms` | List, inspect, state, start/stop/reboot/pause/resume/reset |
| `shares` | List, get, usage |
| `logs` | List, get, system, tail, search |
| `services` | List, get, status |
| `network` | Interfaces and network status |
| `schema` | Inspect API queries, mutations, fields, types |
| `diagnostics` | Ping, latency, env, GraphQL checks, permissions, doctor |
| `auth` | API key management |
| `config` | Profile and config management |
| `completion` | Shell completions |

Run `ucli <group> --help` for detailed syntax.

<details>
<summary>Global flags</summary>

| Flag | Description |
|---|---|
| `--host` | Server URL |
| `--api-key` | API key |
| `--profile` | Config profile name |
| `--output` | `json`, `yaml`, `table`, `human` |
| `--fields` | Comma-separated field list |
| `--filter` | Filter expression (e.g. `state=RUNNING`) |
| `--sort` | Sort expression (e.g. `names:asc`) |
| `--page`, `--page-size`, `--all` | Pagination |
| `--timeout`, `--retry` | Network settings |
| `--quiet`, `--verbose`, `--debug` | Verbosity |
| `--yes`, `--force` | Skip confirmations |

Environment variables supported for host, API key, profile, and config path. Check `ucli diagnostics env` for the exact resolution.

</details>

## Tests

```bash
npm run typecheck    # type checks
npm test             # 385 tests via vitest
npm run build        # compile
```

## Contributing

See `CONTRIBUTING.md` for setup, test commands, and PR guidelines.

## License

MIT. See `LICENSE`.
