# CLI Reference

Command-line interface for building AI agents with the Botpress ADK.

## Quick Start

```bash
# 1. Log in non-interactively when possible
export BOTPRESS_TOKEN=pat_abc123
adk login --token "$BOTPRESS_TOKEN"

# 2. Create a new agent with defaults
adk init my-bot --yes --skip-link
cd my-bot

# 3. Link explicitly when you know the IDs
adk link --workspace ws_123 --bot bot_456

# 4. Start development (CI/agent mode: NDJSON events, no TUI)
adk dev --non-interactive

# 5. Deploy
adk deploy --yes
```

## Commands

### adk init

Create a new ADK agent project.

```bash
adk init [name]
```

**Options:**

- `name` - Project name (optional, prompts if omitted)
- `-t, --template <template>` - Template to use: `blank` or `hello-world`
- `-y, --yes` - Skip prompts and use sensible defaults
- `--defaults` - Alias for `--yes`
- `--skip-link` - Skip the linking step after project creation

**Defaults when using `--yes` / `--defaults`:**

- Project name: `my-agent` (if omitted)
- Template: `hello-world` (if omitted)
- Linking: skipped unless you run `adk link` later

**Examples:**

```bash
adk init customer-support

# Non-interactive setup for AI agents and CI
adk init customer-support --yes --skip-link

# Use the current hello-world template
adk init customer-support --template hello-world
```

**Automation notes:**

- `adk init` installs dependencies automatically after scaffolding.
- The CLI auto-selects a package manager based on lockfiles when possible, otherwise it falls back to the first available manager.
- If authentication is missing, `adk init` may still invoke login first.
- The non-interactive path only works after login has already been completed.
- For unattended setup, log in first with `adk login --token "$BOTPRESS_TOKEN"`, then run `adk init <name> --yes --skip-link`.

**Creates:**

```
my-agent/
├── package.json         # Common ADK scripts and runtime/evals deps
├── tsconfig.json        # Generated type includes
├── .gitignore           # Generated/runtime outputs
├── AGENTS.md            # Assistant instructions
├── CLAUDE.md            # Assistant instructions
├── .agent0/
│   └── capabilities/    # Project-local Agent(0) capability bundle
├── agent.config.ts      # Agent configuration
└── src/
    ├── actions/         # Functions
    ├── conversations/   # Conversation handlers
    ├── knowledge/       # Knowledge bases
    ├── tables/          # Data storage
    ├── triggers/        # Event subscriptions
    └── workflows/       # Long-running processes
```

**Note:** Additional directories like `tools/`, `assets/`, etc. can be created manually as needed.

### adk export

Export the current ADK project as a portable archive.

```bash
adk export [output] [options]
```

**Options:**

- `output` - Archive path (default: `<project-name>.adk`)
- `--no-config` - Omit integration and plugin configuration from dependency snapshots
- `--format <format>` - Output format (`json`)

The archive includes project files plus dependency snapshots for linked dev/prod bots when available. Config is included by default and may contain sensitive values; use `--no-config` before sharing.

### adk import

Import an ADK project archive and link it to new or existing bots.

```bash
adk import <archive> [directory] [options]
```

**Options:**

- `archive` - Archive path created by `adk export`
- `directory` - Destination directory (default: archive project name)
- `--workspace <workspaceId>` - Destination workspace ID
- `--bot <botId>` - Destination production bot ID
- `--dev <devBotId>` - Destination dev bot ID
- `--api-url <apiUrl>` - Botpress API URL
- `-f, --force` - Skip confirmation prompts
- `--package-manager <packageManager>` - `bun`, `pnpm`, `yarn`, or `npm`
- `--format <format>` - Output format (`json`)

Interactive import guides workspace/bot selection and package install. Non-interactive import with `--format json` requires `--workspace`, and applying links/dependency snapshots requires `--force`.

### adk login

Authenticate with Botpress.

```bash
adk login [options]
```

**Options:**

- `--token <token>` - Personal access token
- `--profile <name>` - Profile name (default: "default")
- `--api-url <url>` - API URL (default: https://api.botpress.cloud)

**Examples:**

```bash
# Interactive login
adk login

# Non-interactive with token
adk login --token pat_abc123

# Non-interactive with environment variable
export BOTPRESS_TOKEN=pat_abc123
adk login --token "$BOTPRESS_TOKEN"

# Multiple profiles
adk login --profile staging
adk login --profile production
```

**Automation notes:**

- Preferred AI/CI path: `adk login --token <token>`.
- `BOTPRESS_TOKEN` is best used as `adk login --token "$BOTPRESS_TOKEN"`.
- Bare `BOTPRESS_TOKEN` is only auto-used in non-interactive or no-TTY contexts.
- Without a token, `adk login` falls back to the interactive browser/manual flow.

**Profile Management:**

```bash
adk profiles list          # List all profiles
adk profiles set staging   # Switch profile
```

### adk logout

Remove ADK credentials for the current or a named profile.

```bash
adk logout [options]
```

**Options:**

- `--profile <profile>` - Profile to remove (defaults to the active profile)
- `--format <format>` - Output format (`json`)

```bash
adk logout
adk logout --profile staging
```

### adk dev

Start development mode with hot reloading.

```bash
adk dev [options]
```

**Options:**

- `-p, --port <port>` - Bot port (default: 3000)
- `--port-console <port>` - UI console port (default: 3001)
- `--non-interactive` - Emit structured NDJSON events to stdout without the Ink/TUI (CI/agent-friendly)
- `-v, --verbose` - Show additional details (project path, log file)
- `--otlp` - Enable OTLP trace export to an external collector (default port 4318)
- `--port-otlp <port>` - Port for the OTLP collector endpoint (Jaeger, otel-tui, etc.)

**What it does:**

1. Generates bot project in `.adk/bot/`
2. Creates/restores development bot
3. Syncs tables
4. Checks integrations
5. Registers the agent with the shared Dev Console (starts the singleton if needed)
6. Dev Console available at http://localhost:3001
7. Watches files and hot-reloads

Running `adk dev` in multiple project directories registers each agent with the same Dev Console. Switch between agents in the sidebar. See the [Dev Console multi-agent dashboard](../../adk-dev-console/references/multi-agent-dashboard.md) for details.

**Example:**

```bash
adk dev

# CI / agent mode — NDJSON events to stdout, no TUI
adk dev --non-interactive

# Custom ports in non-interactive mode
adk dev --non-interactive --port 4000 --port-console 4001
```

In `--non-interactive` mode the `lifecycle.ready` event includes `serverPort`, `botPort`, `agentPath`, `healthUrl`, and `botUrl`, so scripts don't need to parse log lines to find them. To discover an already-running Dev Console from a separate process, read `~/.adk/console.port` or run `adk dashboard --no-browser --format json` / `adk ps --format json`.

**Automation notes:**

- `--non-interactive` is the most AI-friendly mode, but `adk dev` is not fully headless.
- Dev can still hit interactive flows such as preflight, knowledge-base sync, or config prompts depending on project state.
- Treat `adk dev` as CI-friendly rather than guaranteed prompt-free.
- Event-driven integrations are not always perfectly mirrored in local dev; if an event flow behaves strangely, verify it against a deployed bot too.

### adk deploy

Deploy agent to Botpress Cloud.

```bash
adk deploy [options]
```

**Options:**

- `-e, --env <environment>` - Target environment (default: "production")
- `-y, --yes` - Auto-approve non-destructive deploy-plan changes without prompting
- `--confirm-storage-changes` - Explicitly confirm destructive table/KB/asset deletions
- `--dry-run` - Compute the deploy plan without applying changes
- `--allow-unconfigured` - Deploy with enabled unconfigured/unresolved dependencies inert instead of blocking
- `--format <format>` - Output format (`json`; requires `--yes` or `--dry-run`)

**What it does:**

1. Runs `adk build`
2. Validates configuration
3. Runs preflight checks
4. Deploys bot to Botpress Cloud
5. Syncs knowledge bases
6. Syncs tables
7. Syncs assets

**Requires:**

- Logged in (`adk login`)
- `agent.json` with botId and workspaceId

**Example:**

```bash
adk deploy

# Auto-approve non-destructive deploy-plan changes
adk deploy --yes

# Preview deploy plan without applying it
adk deploy --dry-run
adk deploy --dry-run --format json
```

**Automation notes:**

- `--yes` auto-approves non-destructive deploy-plan changes.
- Destructive table, KB, or asset deletions still require `--confirm-storage-changes`.
- Enabled dependencies that are unavailable, unconfigured, or unresolved block real deploys unless the user explicitly chooses `--allow-unconfigured`.
- If dev and prod have the same integration alias/name but different versions, deploy prints a non-blocking warning. Preview promotion with `adk integrations copy --from dev --to prod --dry-run` before applying `--yes`.
- JSON output requires either `--yes` or `--dry-run`.
- Deploy still validates configuration and may require interaction if config values are missing.
- Do not assume `adk deploy --yes` is fully non-interactive.

### adk build

Build agent for production.

```bash
adk build
```

Generates types, bundles code, validates configuration.

### adk link

Link local agent to existing remote bot.

```bash
adk link [options]
```

**Options:**

- `--workspace <id>` - Workspace ID
- `--bot <id>` - Bot ID
- `--dev <id>` - Dev bot ID (optional)
- `--api-url <url>` - Botpress API URL (e.g., https://api.botpress.cloud)
- `-f, --force` - Overwrite existing agent.json if present

**Example:**

```bash
# Interactive (recommended)
adk link

# Scriptable when you already know the IDs
adk link --workspace ws_123 --bot bot_456
```

Creates `agent.json` with bot and workspace IDs.

Current project scaffolds do not add `agent.json` to `.gitignore` automatically, so add that manually if your team does not want it committed.

**Automation notes:**

- `adk link --workspace <id> --bot <id>` is the best AI-driven path.
- If only one workspace exists, `adk link` may auto-select it.
- Even with flags, the command still uses the interactive Ink flow internally, so do not assume it is safe in every no-TTY environment.

### adk chat

Chat with your **local development bot**.

> ⚠️ `adk chat` (and `adk chat --single`) targets the linked dev bot — the one started by `adk dev` and identified by `devId`. It does **not** hit the deployed production bot. Never use it as a post-deploy smoke test or as any kind of "did the deploy work?" verification: a `--single` round-trip can pass against the dev bot while production is broken. For deployed bots, use `adk status --format json` for metadata and direct the user to the Dev Console for live verification.

```bash
adk chat [options]
```

**Options:**

- `--single <message>` - Send one message, print the response, and exit
- `--format <format>` - Output format (`json`)
- `--conversation-id <id>` - Continue an existing conversation (use `--format json` to capture the ID from a prior turn)
- `--timeout <duration>` - Max wait duration: `500ms`, `30s`, `1m`, `5m` (default: `60s`)

```bash
adk chat                                          # interactive
adk chat --single '<message>'                     # one-shot
adk chat --single '<message>' --format json
adk chat --single 'Run the full analysis' --timeout 30s
adk chat --single 'Follow up' --conversation-id <id>
```

> **Single-quote the message.** In double quotes the shell expands `$`, so `"I spent $5"` reaches the bot as `I spent ` (and `$10`→`0`, `$84.50`→`4.50`). It looks like the bot can't parse the input, but it's shell mangling. Use single quotes: `adk chat --single 'I spent $5'`.

**Requires:**

- `adk dev` running (also creates the `devId` on first run). Conversation continuation requires the dev server to be running — the user token is persisted automatically.

**Example:**

```bash
adk chat

# Output:
> Hello!
Bot: Hi! How can I help you today?
```

### adk check

Offline validation of the project — schema correctness, ADK convention compliance, integration availability — without contacting Botpress Cloud. Use before `adk dev`, before `adk deploy`, and after any code change.

`adk check` does **not** typecheck your TypeScript — a green `valid: true` does not mean the code compiles. Run `tsc --noEmit` separately to catch type errors before treating work as done.

```bash
adk check [options]
```

**Options:**

- `--format <format>` - Output format: `text` (default) or `json`

**Examples:**

```bash
adk check
adk check --format json    # machine-readable for automation
```

### adk project upgrade

Review and apply ADK project compatibility updates after CLI/runtime upgrades.

```bash
adk project upgrade [options]
```

**Options:**

- `--dry-run` - Review required updates without applying them
- `--format <format>` - Output format (`json`)

Project commands run a runtime preflight before execution. If `@botpress/runtime` is missing, outdated, invalid, or on an unsupported major, the CLI points to `adk project upgrade --dry-run` and then `adk project upgrade`. The upgrade command may update ADK package versions, migrate deprecated integration config object entries to string shorthand when safe, migrate legacy dependency state into Cloud-backed snapshots, and create the project-local Agent(0) capability bundle when missing. If the project runtime is newer than the CLI's supported major, run `adk self-upgrade` instead.

### adk status

Report the project's current link state (workspace + bot), deployed version metadata, and any pending sync issues. Read-only.

```bash
adk status [options]
```

**Options:**

- `--format <format>` - Output format: `text` or `json`

### adk ps

List running ADK dev processes (Dev Console + agents).

```bash
adk ps [options]
```

**Options:**

- `--watch [seconds]` - Continuous refresh (default interval: 2s, not supported with `--format json`)
- `--cloud` - Include Cloud Dev Console prod selections in the listing
- `--wide` - Show all columns (runtime, both PIDs, path)
- `--format <format>` - `text` (default) or `json`

Shows PID, status, uptime, and ports for each process. If none is running, it prints a friendly empty result instead of starting one.

**Example:**

```bash
adk ps
adk ps --wide
adk ps --watch
adk ps --format json
```

### adk dashboard

Open the Dev Console in standalone mode — no agent project required.

```bash
adk dashboard [options]
```

Starts the Dev Console UI server and opens the browser. Useful for connecting to Cloud bots or waiting for agents to register. The standalone Dev Console stays alive even with an empty agent registry.

**Options:**

- `--port-console <port>` - Starting port for the console server (default: 3001)
- `--no-browser` - Do not open the dashboard in a browser (ensures the singleton is running and prints the URL)
- `--format <format>` - Output format (`json`) — emits `{ port, url, wasSpawned }`

```bash
adk dashboard                                # open in browser
adk dashboard --no-browser --format json     # script-friendly: discover the running URL
```

### adk kill

Gracefully stop agents or the entire Dev Console.

```bash
adk kill [agents...] [options]
```

**Options:**

- `--all` - Stop all agents and the Dev Console singleton
- `--current` - Stop the agent in the current working directory
- `--pid <pid>` - Stop a specific process by PID
- `--force` - Escalate to SIGKILL if graceful shutdown fails
- `--dry-run` - Preview what would be stopped without acting

**Examples:**

```bash
adk kill --all              # stop everything
adk kill --current          # stop agent in cwd
adk kill my-agent           # stop by name
adk kill --pid 12345        # stop by PID
adk kill --all --dry-run    # preview
```

### adk logs

Read recent log entries from the linked bot.

```bash
adk logs [level] [options]
```

**Options:**

- `level` - Filter by severity: `error`, `warning`, `info` (positional, optional)
- `--format <format>` - `text` or `json`
- `--follow` - Stream live
- `since=<duration>` - Filter to a recent window (e.g., `since=1h`)

**Examples:**

```bash
adk logs                           # recent entries, all levels
adk logs error --format json       # errors as JSON
adk logs --follow --format json    # stream live
adk logs warning since=1h          # last hour of warnings
```

### adk traces

Read execution traces — tool calls, action invocations, LLM steps, error context — for understanding _what happened_ during a turn, beyond what `adk logs` reports. Reads from the local SQLite trace store under `.adk/`.

```bash
adk traces [tokens...] [options]
```

**Filter tokens** (positional, space-separated):

- `error` — only traces that contain errors
- `workflow=<name>` — filter by workflow name (comma-separated for multiple)
- `action=<name>` — filter by action/tool name
- `trigger=<name>` — filter by trigger name
- `conversation=<id>` — filter by conversation id
- `trace=<id>` — drill into a specific trace (shows the full span tree)
- `since=<duration>` / `until=<duration>` — e.g. `30s`, `5m`, `1h`, `2d`, `1w`
- `limit=<n>` — max traces to show (default: 20)

**Options:**

- `-f, --follow` — stream new traces as they complete
- `--include-llm` — include LLM instructions, code, and tools in drill-in mode
- `--format <format>` — `json` only (omit for default text output)

**Examples:**

```bash
adk traces                                # recent traces
adk traces error                          # error traces only
adk traces workflow=onboarding            # traces for a workflow
adk traces conversation=<id> --format json
adk traces trace=<id> --include-llm       # drill into one trace with LLM content
adk traces since=1h limit=50 --format json
adk traces error --follow                 # stream errors live
```

### adk workflows

Inspect workflow definitions and runs on the linked dev bot. All `adk workflows ...` commands target the dev bot (same credentials path as `adk dev`) and only accept `--format json` — any other `--format` value is rejected.

**Subcommands:**

- `adk workflows` / `adk workflows list` — list discovered workflow definitions
- `adk workflows inspect <name>` — show one workflow's schema and metadata (input schema, schedule, timeout)
- `adk workflows run <name> [payload]` — kick off a run, optionally waiting for it to finish
- `adk workflows runs [tokens...|<wrkflow_id>]` — list runs with filters, or dump status + state + steps for one run by id

#### adk workflows list

```bash
adk workflows                        # list (default)
adk workflows list --format json
```

#### adk workflows inspect

```bash
adk workflows inspect <name> [--format json]
```

Prints the workflow's input schema, description, schedule (if any), and timeout. Use this before `adk workflows run` to see what payload shape it expects.

#### adk workflows run

```bash
adk workflows run <name> [payload] [--wait] [--timeout <duration>] [--format json]
```

**Options:**

- `[payload]` — JSON string, or pipe via stdin (`echo '{...}' | adk workflows run …`)
- `--wait` — block until the run reaches a terminal state
- `--timeout <duration>` — `500ms`, `30s`, `1m`, `5m`; implies `--wait`
- `--format <format>` — only `json` is accepted; any other value is rejected (defaults to `json` if omitted, unlike sibling commands which default to text)

**Examples:**

```bash
adk workflows run onboarding '{"userId":"123"}'
adk workflows run onboarding '{"userId":"123"}' --wait --timeout 30s
echo '{"userId":"123"}' | adk workflows run onboarding --wait
```

#### adk workflows runs

Diagnose durable workflows beyond what `adk logs` and `adk traces` show — list recent runs with filters, or pull the full status + `workflowState` + `workflowSteps` payloads for one run by id.

```bash
adk workflows runs [tokens...|<wrkflow_id>] [--format json]
```

**List filters** (passed as `key=value` tokens):

- `name=<workflowName>` — filter by workflow definition name
- `status=<s1[,s2,...]>` — `pending`, `in_progress`, `failed`, `completed`, `listening`, `paused`, `timedout`, `cancelled`
- `limit=<n>` — cap returned rows
- `nextToken=<token>` — fetch the next page

**Show mode:** pass a workflow instance id (starts with `wrkflow_`) to print one run's metadata plus its `workflowState` and `workflowSteps` payloads. File-swapped payloads are resolved automatically.

**Examples:**

```bash
adk workflows runs                              # recent runs
adk workflows runs name=onboarding              # filter by definition name
adk workflows runs status=failed limit=5        # latest 5 failed runs
adk workflows runs nextToken=<token>            # next page
adk workflows runs wrkflow_01KSF...             # one run (status + state + steps)
```

### adk conversations

List and inspect conversations from the local trace store. Use this to find a conversation id before drilling into it with `adk traces` or `adk conversations show`.

```bash
adk conversations [list] [tokens...] [--format json]
adk conversations show <id> [--include-llm] [--format json]
```

**`list`** (default subcommand) — recent conversations, filtered by positional `key=value` tokens:

- `limit=<n>` - max conversations to show (default: 20)
- `since=<duration>` - only conversations newer than a duration (e.g. `30s`, `5m`, `1h`, `2d`)

**`show <id>`** — full timeline and details for one conversation:

- `--include-llm` - include LLM reasoning spans
- `--format <format>` - output format (`json`)

**Examples:**

```bash
adk conversations                        # recent conversations (list is default)
adk conversations list limit=5
adk conversations list since=1h --format json
adk conversations show <id>              # full timeline
adk conversations show <id> --include-llm --format json
```

**Requires:** `adk dev` run at least once (populates the local trace store).

### adk evals

Run automated conversation tests defined under `evals/`.

```bash
adk evals [name] [options]
```

**Options:**

- `name` - Run a specific eval by name (positional, optional)
- `--tag <tag>` - Filter by tag
- `--type <type>` - Filter by type (e.g., `regression`)
- `--verbose` / `-v` - Show all assertions
- `--format <format>` - `text` (default) or `json`

**Subcommands:**

- `adk evals runs` - List recent runs
- `adk evals runs --latest` - Most recent run
- `adk evals runs --latest -v` - Most recent run with full details

**Examples:**

```bash
adk evals                           # run all evals
adk evals checkout                  # one eval by name
adk evals --tag smoke
adk evals --format json             # for CI
adk evals runs --latest -v
```

### adk integrations

Manage integrations, plugins, and interfaces. Mutation/state subcommands support `--target <env>` (dev or prod, default: dev); use `--format json` where listed for scripted output.

> **Removed aliases:** The old flat commands (`adk add`, `adk remove`, `adk search`, `adk list`, `adk info`, `adk upgrade`) are no longer part of the public CLI. Use `adk integrations ...`.

#### Discovery

```bash
adk integrations search <query>             # Search by keyword
adk integrations search --interface <name>  # Find implementers of an interface
adk integrations list                       # Show installed dependencies
adk integrations info <name[@version]>      # Full integration details
```

**`adk integrations search` options:**

- `--format json` - Machine-readable output
- `--interface <name>` - Find integrations that implement an interface

**`adk integrations list` options:**

- `--format json` - Machine-readable output
- `--verbose` - Show config details

**`adk integrations info` options:**

- `--format json` - Machine-readable output

#### Mutations

```bash
adk integrations add <name>@<version>    # Install integration
adk integrations remove <alias>          # Uninstall integration
adk integrations upgrade <alias>         # Upgrade to latest version
adk integrations enable <alias>          # Enable a disabled integration
adk integrations disable <alias>         # Disable without removing
adk integrations configure <alias>       # Set/unset config values
```

**`adk integrations add` options:**

- `--alias <name>` - Custom alias for code access
- `--target <env>` - Environment (dev/prod)
- `--config key=value` - Set config at install time (repeatable)
- `--format json`

**`adk integrations configure` options:**

- `--set key=value` - Set config values (repeatable)
- `--unset key` - Remove config keys (repeatable)
- `--target <env>` - Environment (dev/prod)

**Examples:**

```bash
# Add with version pin
adk integrations add slack@3.0.0

# Add with alias
adk integrations add openai@1.0.0 --alias ai

# Configure
adk integrations configure slack --set replyBehaviour=start-conversation

# Use env substitution for secrets
adk integrations configure slack --set apiSecret='${env:SLACK_SECRET}'

# Enable
adk integrations enable slack

# Remove
adk integrations remove slack
```

#### State Inspection and Promotion

```bash
adk integrations status                  # Show availability/remediation
adk integrations copy                    # Copy integration state between environments
adk integrations diff                    # Show snapshot vs Cloud differences
```

**`adk integrations status` options:**

- `--target <env>` - Environment (dev/prod)
- `--format json` - Machine-readable output

**`adk integrations copy` options:**

- `--from <env>` - Source environment
- `--to <env>` - Target environment
- `--dry-run` - Preview without applying
- `--yes` - Skip confirmation for prod/destructive changes

### adk plugins

Manage plugins (reusable agent extensions). Mirrors the `adk integrations` subcommand structure. Mutation/state subcommands support `--target <env>`; use `--format json` where listed for scripted output.

```bash
adk plugins search <query>               # Search by keyword
adk plugins list                         # Show installed plugins
adk plugins info <name>                  # Full plugin details
adk plugins add <name>@<version>         # Install plugin
adk plugins remove <alias>               # Uninstall plugin
adk plugins upgrade <alias>              # Upgrade version
adk plugins enable <alias>               # Enable a disabled plugin
adk plugins disable <alias>              # Disable without removing
adk plugins configure <alias>            # Set config and interface mappings
adk plugins status                       # Show availability/remediation
adk plugins copy                         # Copy state between environments
adk plugins diff                         # Show snapshot vs Cloud differences
```

**Plugin-specific flags:**

- `adk plugins add --dep iface=alias` - Wire interface dependency (repeatable)
- `adk plugins configure --map iface=alias` - Remap interface dependency

**Shared with `adk integrations upgrade`:**

- `--to <version>` - Target specific version

Plugins require interfaces implemented by installed integrations. The CLI auto-resolves dependencies when unambiguous. See **[Plugins](./plugins.md)** for details.

### adk dependencies

Export or import dependency-only snapshots for integrations and plugins.

```bash
adk dependencies export [output] [options]
adk dependencies import <file> [options]
```

**`adk dependencies export` options:**

- `output` - Snapshot path (default: `<project-name>.dependencies.<target>.json`)
- `--target <env>` - `dev` or `prod` (default: `dev`)
- `--no-config` - Omit integration and plugin configuration
- `--format <format>` - `text` or `json`

**`adk dependencies import` options:**

- `file` - Snapshot path created by `adk dependencies export`
- `--target <env>` - `dev` or `prod` (default: snapshot env)
- `--dry-run` - Show what would change without writing
- `--yes` - Allow prod or destructive changes without confirmation
- `--format <format>` - `text` or `json`

These artifacts are explicit backups or transfer files. They are not replacements for generated `.adk/dependencies/dev.json` or `.adk/dependencies/prod.json`.

### adk self-upgrade

Upgrade the ADK CLI itself to the latest version.

```bash
adk self-upgrade
```

**Aliases:** `adk self-update`

**What it does:**

1. Checks npm registry for latest version
2. Downloads binary from GitHub releases
3. Replaces current CLI executable
4. Verifies installation

**Example:**

```bash
adk self-upgrade

# Output:
📦 Current version: 1.13.10
📦 Latest version: 1.13.16
📥 Downloading adk v1.13.16 for darwin-arm64...
✅ Successfully upgraded!

   v1.13.10 → v1.13.16

   Run adk --version to verify
```

**Note:** The ADK automatically checks for updates every 24 hours and shows a notification when a new version is available. On Windows, you may need to restart your terminal after upgrading.

**This is different from `adk integrations upgrade` / `adk plugins upgrade`**, which upgrade installed dependencies, not the CLI itself.

### adk kb

Manage knowledge bases and synchronization.

```bash
adk kb sync [options]
```

**Commands:**

- `adk kb sync` - Sync knowledge base sources with remote

**Options:**

- `--dev` - Sync with development bot (required: must use --dev or --prod)
- `--prod` - Sync with production bot (required: must use --dev or --prod)
- `--dry-run` - Preview changes without applying them
- `-y, --yes` - Skip confirmation prompts
- `--confirm-storage-changes` - Confirm destructive storage changes (KB deletions)
- `--force` - Force re-sync all knowledge bases
- `--format <format>` - Output format (`json`; requires `--yes`)

**What it does:**

1. Detects knowledge bases defined in your project
2. Identifies sources (directories, websites, tables)
3. Syncs content to Botpress Cloud
4. Handles orphaned sources (sources removed from code)

**Example:**

```bash
# Sync to development bot
adk kb sync --dev

# Sync to production bot
adk kb sync --prod

# Auto-confirm sync
adk kb sync --dev -y
adk kb sync --dev -y --format json

# Preview changes without applying
adk kb sync --dev --dry-run

# Force re-sync all knowledge bases
adk kb sync --dev --force
```

**Source Types:**

- `Directory` - Local files from a directory
- `Website` - Pages from sitemap or URLs
- `Table` - Data from bot tables

**Note:** KB sync is also run automatically during `adk dev` and `adk deploy`.

### adk assets sync

Sync assets with remote storage.

```bash
adk assets sync [options]
```

**Options:**

- `--dry-run` - Preview changes
- `-y, --yes` - Skip confirmation
- `--bail-on-failure` - Stop on first error
- `--force` - Force re-upload all files
- `--format <format>` - Output format (`json`; requires `--yes`)

**Example:**

```bash
# Interactive
adk assets sync

# Auto-confirm
adk assets sync -y
adk assets sync -y --format json
```

**Other asset commands:**

```bash
adk assets list          # List all assets
adk assets status        # Show sync status
adk assets pull          # Download remote assets to local directory
```

### adk assets list

List all asset files.

```bash
adk assets list [options]
```

**Options:**

- `--local` - Show only local assets
- `--remote` - Show only remote assets
- `--format <format>` - Output format (`json`)

### adk assets status

Show asset synchronization status.

```bash
adk assets status [--format json]
```

### adk assets pull

Download remote assets to local directory.

```bash
adk assets pull
```

### adk mcp

Start the MCP (Model Context Protocol) server for AI assistant integration.

```bash
adk mcp [--cwd <path>]
```

The MCP server provides tools for AI assistants (Claude Code, Cursor, VS Code) to debug, test, and manage your ADK project. See **[MCP Server](./mcp-server.md)** for details.

### adk mcp:init

Generate MCP configuration files for AI assistants.

```bash
adk mcp:init [options]
```

**Options:**

- `--all` - Generate for all supported tools
- `--tool <name>` - Generate for specific tool (claude-code, vscode, cursor)
- `--force` - Overwrite existing config
- `--project-dir <path>` - ADK project subdirectory (for monorepos)

**Example:**

```bash
adk mcp:init --all
```

See **[MCP Server](./mcp-server.md)** for monorepo setup and troubleshooting.

### adk profiles

Manage authentication profiles.

```bash
adk profiles [command]
```

**Commands:**

- `adk profiles list` - List all configured profiles
- `adk profiles set [profile]` - Switch to a different profile

**Example:**

```bash
# List all profiles
adk profiles list

# Switch to a different profile
adk profiles set staging
```

### adk config

Configure agent settings interactively.

```bash
adk config [options]
```

**Options:**

- `--prod` - Use production configuration

**Subcommands:**

- `adk config:get <key>` - Get a configuration value
- `adk config:set <key> <value>` - Set a configuration value

Both subcommands support `--prod` flag for production configuration.

**Example:**

```bash
# Interactive configuration
adk config

# Get a config value
adk config:get botId

# Set a config value
adk config:set botId bot_123

# Use production configuration
adk config --prod
adk config:get botId --prod
```

**Note:** This replaces the legacy `adk agent` command.

### adk secret

Manage the bot's secrets in the local store. `adk secret` (no subcommand) shows the declared secrets and whether each is set.

```bash
adk secret [options]                      # show declared secrets + status
adk secret:set <key> <value> [options]    # set a secret value
adk secret:delete <key> [options]         # delete a secret
```

**Options (all three):**

- `--prod` - Target the production bot (default: dev)
- `--format <format>` - Output format (`json`)

`<key>` is `SCREAMING_SNAKE_CASE`. `secret:set` never echoes the value back.

```bash
adk secret                                # list declared secrets and set/unset status
adk secret --prod --format json
adk secret:set OPENAI_API_KEY sk-...      # set on the dev bot
adk secret:delete OPENAI_API_KEY --prod   # delete on the prod bot
```

### adk models

List the Cognitive models available to the current bot, grouped by integration (including aliases like `fast` and `best`). Useful when configuring model selection or diagnosing a model-not-found error.

```bash
adk models [--format json]
```

### adk telemetry

Manage telemetry preferences.

```bash
adk telemetry [options]
```

**Options:**

- `--status` - Show telemetry status
- `--enable` - Enable telemetry
- `--disable` - Disable telemetry

**Example:**

```bash
# Check telemetry status
adk telemetry --status

# Enable telemetry
adk telemetry --enable

# Disable telemetry
adk telemetry --disable
```

### adk run

Run a TypeScript script with full ADK runtime context.

```bash
adk run <script> [args...] [options]
```

**Options:**

- `--force` - Force regeneration of the bot project
- `--prod` - Use production bot ID instead of dev bot ID

**Description:**

Executes a TypeScript script with access to the full ADK runtime, including:

- Bot client with authentication
- All tables, workflows, and actions from your project
- Type-safe access to your bot's configuration

**Use Cases:**

- One-off data migrations
- Manual sync operations
- Testing specific functionality
- Admin scripts

**Example Scripts:**

```typescript
// scripts/migrate-users.ts
import { UsersTable } from '../src/tables/Users'

const { rows } = await UsersTable.findRows({ limit: 100 })

for (const user of rows) {
  await UsersTable.updateRows({
    rows: [{ id: user.id, migrated: true }],
  })
  console.log(`Migrated user: ${user.id}`)
}

console.log(`✅ Migrated ${rows.length} users`)
```

**Examples:**

```bash
# Run a migration script
adk run scripts/migrate-users.ts

# Run with production bot
adk run scripts/sync-data.ts --prod

# Force regenerate types before running
adk run scripts/fix-data.ts --force

# Pass arguments to your script
adk run scripts/process.ts arg1 arg2
```

**Requirements:**

- Must be logged in (`adk login`)
- Must have linked bot (`adk link`)
- Script must be a TypeScript file

### Global Options

```bash
adk --no-cache <command>    # Disable cache
adk --version               # Show version
adk --help                  # Show help
adk                         # In agent directory: runs 'adk dev', otherwise: shows welcome
```

## Common Workflows

### New Project

```bash
adk init my-bot
cd my-bot
bun install
adk login
adk dev
```

### Daily Development

```bash
# Start dev
adk dev

# Make changes (auto-reload)

# Test
adk chat

# Deploy when ready
adk deploy
```

### Working with Existing Bot

```bash
git clone <repo>
cd my-bot
bun install
adk login
adk link --workspace ws_123 --bot bot_456
adk dev
```

### Managing Integrations

```bash
# Search for integrations
adk integrations search slack

# Find integrations that implement an interface
adk integrations search --interface hitl

# Get detailed info about an integration
adk integrations info slack

# Add
adk integrations add slack@3.0.0

# Configure
adk integrations configure slack --set replyBehaviour=start-conversation

# Enable and start dev server for OAuth
adk integrations enable slack
adk dev  # Complete OAuth in Dev Console at localhost:3001

# List installed
adk integrations list

# Remove
adk integrations remove slack
```

## Best Practices

**DO:**

- Use `adk dev` for development (hot reload)
- Keep `agent.config.ts` in git
- Use `.env` for secrets
- Run `adk chat` for quick testing

**DON'T:**

- Don't edit `.adk/` directory (auto-generated) — **except** `.adk/scratch/`, which is reserved for disposable user/agent files (one-off runners, throwaway probes). `adk dev` does not touch `.adk/scratch/`. Production code, persistent helpers, and anything you'd commit belong outside `.adk/`.
- Don't commit `agent.json` (add to .gitignore)
- Don't commit `.env` files
- Don't skip integration configuration in UI

## Quick Reference

```bash
# Lifecycle
adk init <name>          # Create project
adk login                # Authenticate
adk link                 # Link to remote bot
adk dev                  # Start development
adk chat                 # Test interactively
adk deploy               # Deploy to production
adk run <script>         # Run script with ADK runtime

# Multi-Agent / Dev Console
adk ps                   # List running agents and processes
adk dashboard            # Open Dev Console standalone (no agent needed)
adk kill --all           # Stop all agents + Dev Console

# Diagnostics (local trace store)
adk logs                 # Recent log entries
adk traces               # Execution traces
adk conversations        # List recent conversations
adk conversations show <id>  # Inspect one conversation timeline

# Workflows
adk workflows            # List discovered workflows
adk workflows inspect <name>  # Inspect workflow schema
adk workflows run <name>      # Start a workflow
adk workflows runs            # List or inspect workflow runs

# Dependencies (integrations, plugins, interfaces)
adk integrations search <query>    # Search for integrations
adk integrations list              # List installed dependencies
adk integrations info <name>       # Show integration details
adk integrations add <name>@<ver>  # Add integration
adk integrations remove <alias>    # Remove integration
adk integrations upgrade <alias>   # Upgrade dependency
adk integrations enable <alias>    # Enable integration
adk integrations disable <alias>   # Disable integration
adk integrations configure <alias> # Set/unset config values
adk integrations status            # Show availability/remediation
adk integrations copy --from dev --to prod --dry-run  # Preview promotion
adk integrations diff              # Show snapshot vs Cloud differences

# Plugins
adk plugins search <query>        # Search for plugins
adk plugins list                   # List installed plugins
adk plugins add <name>@<version>   # Add plugin
adk plugins remove <alias>         # Remove plugin
adk plugins configure <alias>      # Set config / remap interfaces
adk plugins status                 # Show availability/remediation
adk plugins copy --from dev --to prod --dry-run  # Preview promotion
adk plugins diff                   # Show snapshot vs Cloud differences

# Dependency import/export (integrations + plugins)
adk dependencies export            # Export dev dependency state
adk dependencies export --target prod --no-config
adk dependencies import <file> --dry-run
adk dependencies import <file> --target prod --yes

# Project portability and compatibility
adk export                         # Export a portable .adk project archive
adk import <archive>               # Import an ADK project archive
adk project upgrade --dry-run      # Review project compatibility updates
adk project upgrade                # Apply project compatibility updates

# MCP (AI Assistant Integration)
adk mcp                  # Start MCP server
adk mcp:init --all       # Generate MCP config files

# CLI Management
adk self-upgrade         # Upgrade ADK CLI itself
adk telemetry            # Manage telemetry preferences

# Authentication
adk profiles list        # List profiles
adk profiles set         # Switch profile
adk logout               # Remove credentials for a profile

# Configuration
adk config               # Configure agent settings
adk config:get <key>     # Get config value
adk config:set <key> <value>  # Set config value
adk secret               # Show declared secrets + status
adk secret:set <k> <v>   # Set a secret
adk models               # List available Cognitive models

# Workflows (dev bot only; --format json only)
adk workflows                     # List workflow definitions
adk workflows inspect <name>      # Show one workflow's schema + metadata
adk workflows run <name> [json]   # Run a workflow (add --wait to block)
adk workflows runs                # List recent workflow runs
adk workflows runs <wrkflow_id>   # Inspect one run (status + state + steps)

# Knowledge Bases
adk kb sync --dev        # Sync KB to development bot
adk kb sync --prod       # Sync KB to production bot

# Assets
adk assets sync          # Sync assets
adk assets list          # List all assets
adk assets status        # Check sync status
adk assets pull          # Download remote assets
```

## See Also

- **[Agent Configuration](./agent-config.md)** - agent.config.ts, agent.json, environment variables, and project files
- **[MCP Server](./mcp-server.md)** - AI assistant integration (Claude Code, Cursor, VS Code)
- **[Conversations](./conversations.md)** - Conversation handlers
- **[Workflows](./workflows.md)** - Long-running processes
- **[Patterns & Mistakes](./patterns-mistakes.md)** - Best practices
