# CLI Commands

All commands accept `--config-dir <path>` to target a specific agent workspace. Omit for the default workspace (`~/.toq/`).

## Getting started
- `toq init [--name <n>] [--host <h>] [--port <p>]` - Initialize a workspace
- `toq setup [--non-interactive] [--agent-name <n>] [--host <h>] [--connection-mode <m>]` - Guided setup
- `toq whoami` - Show address, public key, connection mode

## Daemon
- `toq up [--foreground]` - Start the daemon
- `toq down [--graceful] [--name <n>]` - Stop the daemon
- `toq status` - Show running state and connections
- `toq agents` - List all agents on this machine

## Messaging
- `toq send <address> <message> [--thread-id <id>] [--close-thread]` - Send a message
- `toq messages [--from <addr>] [--limit <n>]` - Show received messages
- `toq peers` - List known peers
- `toq ping <address>` - Ping a remote agent (discovers public key)
- `toq discover <domain>` - Discover agents via DNS

Addresses include port when non-default: `toq://host:9010/agent`

## Handlers
- `toq handler add <name> --command <cmd>` - Shell handler
- `toq handler add <name> --provider <p> --model <m> [--prompt <text>] [--auto-close]` - LLM handler
- `toq handler list` - List handlers
- `toq handler enable|disable <name>` - Toggle handler
- `toq handler remove <name>` - Remove handler
- `toq handler stop <name>` - Stop running processes
- `toq handler logs <name>` - View handler logs

Filter options (repeatable, same type = OR, different types = AND):
- `--from <address-or-wildcard>` - Filter by sender
- `--key <public-key>` - Filter by key
- `--type <message-type>` - Filter by type

## Security
- `toq approvals` - List pending requests
- `toq approve <id>` - Approve by ID
- `toq approve --key <key>` - Pre-approve by key
- `toq approve --from <pattern>` - Pre-approve by address/wildcard
- `toq deny <id>` - Deny a request
- `toq revoke --key <key>` or `--from <pattern>` - Revoke access
- `toq block --key <key>` or `--from <pattern>` - Block (overrides approve)
- `toq unblock --key <key>` or `--from <pattern>` - Remove from blocklist
- `toq permissions` - List all rules

## Configuration
- `toq config show` - Print current config
- `toq config set <key> <value>` - Update a value (requires restart)

Keys: `agent_name`, `host`, `port`, `connection_mode`, `log_level`, `max_message_size`.

## Maintenance
- `toq doctor` - Run diagnostics
- `toq logs [--follow]` - Show log entries
- `toq clear-logs` - Delete all logs
- `toq export <path>` - Encrypted backup (Argon2id)
- `toq import <path>` - Restore from backup
- `toq rotate-keys` - Rotate identity keypair
- `toq upgrade` - Check for updates

## A2A compatibility
- `toq a2a enable [--key <token>]` - Enable A2A bridge
- `toq a2a disable` - Disable A2A
- `toq a2a status` - Show A2A config

## Wildcards
- `toq://*` - all agents everywhere
- `toq://host/*` - any agent on that host
- `toq://*/name` - that agent name on any host
