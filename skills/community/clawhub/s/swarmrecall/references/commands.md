# CLI commands — full reference

All commands support `--help` for per-command flag documentation. Global commands:

## Setup

| Command | Description |
| --- | --- |
| `swarmrecall register [--name <n>] [--save]` | Register a new agent. `--save` writes the API key to `~/.config/swarmrecall/config.json`. |
| `swarmrecall config set-key <key>` | Set API key. |
| `swarmrecall config set-url <url>` | Override API base URL. |
| `swarmrecall config show` | Print current config. |

## MCP server

| Command | Description |
| --- | --- |
| `swarmrecall mcp` | Run the MCP server over stdio. Point MCP clients at this command. Reads `SWARMRECALL_API_KEY` / config file for auth. |

## Memory

| Command | Description |
| --- | --- |
| `swarmrecall memory store <content> [-c <cat>] [-i <imp>] [-t <tags>] [-p <pool>]` | Store a memory. |
| `swarmrecall memory search <query> [-l <n>]` | Semantic search. |
| `swarmrecall memory list [-c <cat>] [-l <n>]` | List memories. |
| `swarmrecall memory sessions list` | List sessions. |
| `swarmrecall memory sessions current` | Fetch active session. |

## Knowledge

| Command | Description |
| --- | --- |
| `swarmrecall knowledge create --type <t> --name <n> [--props <json>] [-p <pool>]` | Create entity. |
| `swarmrecall knowledge search <query>` | Semantic search over entities. |
| `swarmrecall knowledge traverse --from <id> [--rel <r>] [--depth <n>]` | Walk the graph. |

## Learnings

| Command | Description |
| --- | --- |
| `swarmrecall learnings log --category <c> --summary <s> [--details <d>] [--priority <p>] [--area <a>] [-p <pool>]` | Log a learning. |
| `swarmrecall learnings patterns` | List recurring patterns. |
| `swarmrecall learnings promotions` | List promotion candidates. |

## Skills

| Command | Description |
| --- | --- |
| `swarmrecall skills list [--status <s>]` | List registered skills. |
| `swarmrecall skills register --name <n> [--source <s>] [--version <v>] [-p <pool>]` | Register a skill. |

## Pools

| Command | Description |
| --- | --- |
| `swarmrecall pools list` | Pools this agent belongs to. |
| `swarmrecall pools show <poolId>` | Pool details + members. |

## Dream

| Command | Description |
| --- | --- |
| `swarmrecall dream start [--ops <o>] [--dry-run]` | Start a cycle. |
| `swarmrecall dream status` | Show the last cycle. |
| `swarmrecall dream config [--enable] [--disable] [--interval <h>]` | Show or update dream config. |
| `swarmrecall dream candidates <type> [-l <n>]` | List candidates (duplicates \| stale \| contradictions \| unsummarized-sessions \| duplicate-entities \| unprocessed). |
| `swarmrecall dream execute [--ops <o>]` | Run Tier 1 ops (decay, prune, cleanup). |

## Environment

- `SWARMRECALL_API_KEY` — API key; takes precedence over config file.
- `SWARMRECALL_API_URL` — API base URL; defaults to `https://swarmrecall-api.onrender.com`.
