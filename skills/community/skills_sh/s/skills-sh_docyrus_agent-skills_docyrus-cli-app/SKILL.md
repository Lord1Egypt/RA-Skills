---
name: docyrus-cli-app
description: Use the Docyrus CLI (`docyrus`) to interact with the Docyrus platform from the terminal. Use when the user asks to authenticate, list apps, query or manage data records (`ds`), manage dev app data source schema objects (`studio`) including data sources, fields, enums, data views, forms, webforms, HTML/PDF export templates, and email templates, manage automations and their triggers/action nodes (`automation`), build or edit custom AI agents and their sub-resources (`agent`), set an app's AI agent context or manage app-scoped AI tools (`apps`), list tenant email accounts and send emails (`messaging`), manage tenant account settings — brands, the current user's profile, and tenant regional/formatting preferences (`account`), discover and call connectors (`connect`), send API requests, switch tenants/accounts, discover tenant OpenAPI specs, drive browser automation (`browser`), chat with platform agents (`docy`), launch the pi cowork/coding agents (`opsy`/`cody`/`coder`), run the agent bridge server (`server`), manage the repo knowledge graph (`knowledge`) and project plan (`project-plan`), cut releases (`release`), or use the terminal UI via `docyrus tui`. Triggers on `docyrus ds list`, `docyrus ds comments`, `docyrus ds files upload`, `docyrus studio`, `docyrus studio search-fields`, `docyrus automation`, `docyrus automation create-node`, `docyrus agent`, `docyrus apps set-agent-context`, `docyrus apps ai-tools`, `docyrus messaging email send`, `docyrus account brands`, `docyrus account user-profile`, `docyrus account tenant-preferences`, `docyrus connect`, `docyrus discover`, `docyrus auth`, `docyrus browser`, `docyrus knowledge`, `docyrus project-plan`, `docyrus release`, `docyrus server`, `docyrus tui`, or any terminal-based Docyrus workflow.
---

# Docyrus CLI

Command index for the `docyrus` CLI (`@docyrus/docyrus`). This skill is a **quick reference to what commands exist**. For exact flags, arguments, and payload shapes of any command, **run its help** — that is the authoritative, always-current source:

```bash
docyrus <command> --help                 # flags + args for a command or group
docyrus <command> <subcommand> --help     # drill into a subcommand
docyrus <command> --llms                  # machine-readable (LLM) manifest of a command tree
```

## Conventions (apply across all commands)

- **Output:** add `--json` (or `--format <toon|json|yaml|md|jsonl>`) for machine-readable output; `--verbose` shows the full envelope.
- **Flag forms:** `--help` prints flags in kebab-case (`--app-slug`, `--from-file`); the parser also accepts the camelCase schema keys (`--appSlug`, `--fromFile`). Both work.
- **Selectors are exclusive pairs** — pass exactly one of each; the CLI resolves the other: `--appId | --appSlug`, `--dataSourceId | --dataSourceSlug`, `--fieldId | --fieldSlug`, etc.
- **Write payloads:** mutating commands take convenience flags **and/or** `--data '<json>'` / `--from-file <path.json>`. Explicit flags merge over the JSON. Complex objects (nested `data`, `field_mapping`, schemas, conditions) must go through `--data`/`--from-file`.
- **Settings scope & sessions:** settings live in a project-local `./.docyrus/` folder (ancestor-resolved from cwd); `-g`/`--global` uses `~/.docyrus/`. Auth and the active tenant are per-scope.
- **Escape hatch:** `docyrus curl <path> [-X .. -d .. -G]` sends an authenticated request to any API path — use it for endpoints without a dedicated command (e.g. template render, webform items).

## Command index

Run `docyrus <command> --help` for flags. Groups marked **(group)** have their own subcommands — drill in with `--help`.

### auth — authentication, accounts, tenants
`login` · `logout` · `who` · `tenant` · `set-tokens` · `sso-session` · `github` · `sandbox` · `git-credential` · `accounts` (group) · `tenants` (group)

### apps — apps & app-scoped resources
`list` · `update` · `delete` · `restore` · `permanent-delete` · `set-agent-context` · `actions` (group: action CRUD + run) · `ai-tools` (group: app-scoped AI tool CRUD — see **docyrus-app-ai-tools**)

### ds — data records (CRUD + sub-objects)
`get` (data source metadata) · `list` (query records) · `create` · `update` · `delete` · `comments` (group: record comments) · `files` (group: record file attachments, incl. `upload`)

### dsql — logical SQL querying
`query` (read-only SELECT over `appSlug.dataSourceSlug`) · `ask` (NL → query → run) · `generate` (NL → query, no run) · `schema` (group: schema discovery). See **docyrus-dsql-query-design**.

### studio — dev app schema CRUD
Data sources: `create-data-source` · `get-data-source` · `update-data-source` · `delete-data-source` · `restore-data-source` · `permanent-delete-data-source` · `list-data-sources` · `bulk-create-data-sources`
Fields: `create-field` · `get-field` · `update-field` · `delete-field` · `list-fields` · `create-fields-batch` · `update-fields-batch` · `delete-fields-batch` · `search-fields`
Enums: `create-enums` · `update-enums` · `delete-enums` · `list-enums` · `search-enums` · `search-enum-sets`
Data views: `create-data-view` · `get-data-view` · `update-data-view` · `delete-data-view` · `list-data-views`
Forms: `create-form` · `get-form` · `update-form` · `delete-form` · `list-forms`
Webforms: `create-webform` · `get-webform` · `update-webform` · `delete-webform` · `list-webforms` (see **docyrus-webform-design**)
HTML/PDF templates: `create-html-template` · `get-html-template` · `update-html-template` · `delete-html-template` · `list-html-templates` (see **docyrus-print-pdf-template-design**)
Email templates: `create-email-template` · `get-email-template` · `update-email-template` · `delete-email-template` · `list-email-templates` (see **docyrus-email-template-design**)
→ Design how-to: **docyrus-data-source-design**.

### automation — workflows
Automations: `create` · `get` · `update` · `delete` · `list`
Triggers: `create-trigger` · `update-trigger` · `delete-trigger` · `get-trigger` · `list-triggers`
Action nodes: `create-node` · `update-node` · `delete-node` · `get-node` · `list-nodes`
→ Design how-to: **docyrus-automation-design**.

### agent — custom AI agents & sub-resources
Agent: `create` · `get` · `update` · `delete` · `list` · `upload`
Sub-resource groups (each list/get/create/update/delete): `models` · `tools` · `data-sources` · `docs` · `mcps` · `connections` · `dynamic-contexts` · `workflow-steps` · `deployments` · `deployment-tools` · `deployment-data-sources` · `workflow-jobs` (read-only + delete) · `tasks` · `recurring-tasks`
→ Design how-to: **docyrus-agent-design**.

### messaging — email & notifications
`accounts` (list tenant email accounts) · `email` (group: incl. `send`)

### account — tenant account management
`brands` (group: tenant brand CRUD — `list` · `get` · `create` · `update` · `delete` · `fetch-from-website`) · `user-profile` (group: `get` · `update` the current user's own profile) · `tenant-preferences` (group: `get` · `update` the tenant's regional/formatting preferences)

- **`brands`** — the tenant's visual identity, typography, voice, and content guidelines (`tenant_brand`). `create`/`update` take camelCase convenience flags (1:1 with the snake_case DTO keys) plus `--data` / `--from-file`; `--name` is required on `create`. → Manage how-to (incl. full field catalog): **docyrus-tenant-brand-management**.
- **`user-profile`** — the authenticated user's own profile (`get`/`update`, no selector). `update` flags cover the self-service fields: `--firstname` · `--lastname` · `--mobile` · `--dateOfBirth` · `--gender` · `--timeZone` · `--language`.
- **`tenant-preferences`** — the workspace's regional/formatting settings. `update` is tenant-admin only and takes camelCase flags (1:1 with the snake_case `--data` keys) plus `--data` / `--from-file`: `--language` · `--locale` · `--timeZone` · `--startWeekOn` · `--fiscalYear` · `--dateFormat` · `--dateTimeFormat` · `--timeFormat` · `--longDateFormat` · `--businessHoursBegin` · `--businessHoursEnd` · `--dailyWorkingHours` (seconds) · `--weeklyWorkingCapacity` · `--timeRounding` · `--baseCurrency` · `--currencyAbbrPosition` (`BEFORE`/`AFTER`) · `--decimalPrecision` · `--decimalSeparator` · `--thousandSeparator`. `get` returns just the preferences record (camelCase keys).

→ `user-profile` / `tenant-preferences` how-to (incl. full field catalog): **docyrus-account-settings**.

### connect — connectors & actions
`list-connectors` · `get-connector` · `list-connections` · `get-action` · `run-action` · `curl` (request through a connector's provider auth)
→ Usage how-to: **docyrus-integrations-and-connectors**.

### discover — tenant OpenAPI discovery
`api` (download spec) · `namespaces` · `path` · `endpoint` · `entity` · `search`

### curl — raw API
`docyrus curl <path> [-X <method>] [-d <body>] [-G] [-H <header>]` — authenticated request to any Docyrus API path.

### AI agents & runtime
`docy "<prompt>"` (chat with the platform's main AI agent) · `opsy` (pi Cowork agent) · `cody` / `coder` (pi Coding agent) · `server` (HTTP bridge from a pi agent to AI SDK `useChat`)

### browser — browser automation (local Chrome or remote Cloudflare)
`start` · `nav` · `snapshot` · `click` · `fill` · `select` · `eval` · `run-script` · `screenshot` · `content` · `console` · `network` · `cookies` · `devtools` · `info` · `tabs` · `wait` · `close`

### knowledge — repo knowledge graph (dev tooling)
`search` · `section` · `locate` · `refs` · `expand` · `check` · `doctor` · `audit-staged` · `pre-commit` · `list-impacted` · `init` · `generate-initial` · `refresh` · `config` · `hook`

### project-plan — repo-tracked project plan (dev tooling)
`show` · `summary` · `list-phases` · `list-features` · `list-tasks` · `find-tasks` · `get-task` · `upsert-phase` · `upsert-feature` · `upsert-task` · `set-task-status` · `set-order` · `ensure` · `check` · `config` · `create-linked-todo` · `upsert-from-architect` · `upsert-from-plan`

### release — versioning
`new-version` · `status`

### tui — terminal UI
`docyrus tui` — launch the OpenTUI terminal UI (requires Bun).

### Built-ins
`docyrus completions` (shell completion) · `docyrus mcp add` (register as MCP server) · `docyrus skills add` (sync skill files) · global `--mcp` (start as MCP stdio server).

## Related skills

For *designing* the things these commands manage, use the dedicated skills: **docyrus-data-source-design**, **docyrus-automation-design**, **docyrus-agent-design**, **docyrus-app-ai-tools**, **docyrus-email-template-design**, **docyrus-print-pdf-template-design**, **docyrus-webform-design**, **docyrus-acl-design** (`docyrus acl`), **docyrus-tenant-brand-management** (`docyrus account brands`), **docyrus-account-settings** (`docyrus account user-profile` / `tenant-preferences`), **docyrus-dsql-query-design**. For platform architecture/concepts: **docyrus-platform**. For the REST API in app code: **docyrus-api-dev**.
