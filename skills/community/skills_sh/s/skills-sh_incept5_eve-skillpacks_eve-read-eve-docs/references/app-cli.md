# App CLI Reference

Eve-compatible apps can ship domain-specific CLIs that agents use instead of raw REST API calls. This reference covers the manifest schema, environment variable contract, distribution mechanisms, and implementation patterns.

## Manifest Schema

Declare a CLI on any service with an `x-eve.cli` block:

```yaml
services:
  api:
    build:
      context: ./apps/api
    ports: [3000]
    x-eve:
      api_spec:
        type: openapi
      cli:
        name: myapp           # Required — binary name on $PATH
        bin: cli/bin/myapp     # Required (repo mode) — path relative to repo root
        image: org/cli:tag     # Alternative (image mode) — Docker image
        description: "..."     # Optional — shown in agent instruction block
```

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | CLI binary name. Lowercase alphanumeric + hyphens. Must be unique per project. |
| `bin` | string | Yes (repo mode) | Path to executable, relative to repo root. |
| `image` | string | Yes (image mode) | Docker image containing CLI at `/cli/bin/{name}`. |
| `description` | string | No | Brief description for agent instruction block. |

Use `bin` for Node.js/script CLIs (zero latency). Use `image` for compiled Go/Rust CLIs (2-5s init container latency).

## Cross-Project App-Link CLIs

When a producer project exports an API through `x-eve.app_links.exports.apis`
and includes `cli: <name>`, the referenced service must declare a matching
`x-eve.cli.name` and an `image`. Cross-project app links always use image mode:
the consumer job/service does not have the producer repository checked out, so a
repo-bundled `bin` path is not enough.

```yaml
services:
  api:
    image: ghcr.io/acme/producer-api:latest
    x-eve:
      api_spec:
        type: openapi
        spec_url: /openapi.json
      cli:
        name: observations
        bin: observations
        image: ghcr.io/acme/observations-cli:latest

x-eve:
  app_links:
    exports:
      apis:
        observation:
          service: api
          cli: observations
          scopes: [observations:read]
          consumers:
            - project: consumer
              scopes: [observations:read]
```

Consumer jobs/services receive the producer CLI on `PATH` and the pointer
`EVE_APP_LINK_<ALIAS>_CLI=<cli-name>` when the subscription resolves. The CLI
should read `EVE_APP_LINK_<ALIAS>_API_URL` and
`EVE_APP_LINK_<ALIAS>_TOKEN` to call the producer API.

## Environment Variable Contract

The platform injects these env vars into every agent job with `with_apis`:

| Variable | Example | Source |
|----------|---------|--------|
| `EVE_APP_API_URL_{SERVICE}` | `http://api.svc:3000` | Platform, from `resolved_app_apis` |
| `EVE_JOB_TOKEN` | `eyJhbGciOi...` | Platform, minted per job (RS256 JWT) |
| `EVE_PROJECT_ID` | `proj_abc123` | Platform, from job context |
| `EVE_ORG_ID` | `org_xyz789` | Platform, from job context |

The CLI reads these directly — no configuration files, no login commands, no manual setup.

### Service Name → Env Var Mapping

The env var name is derived from the manifest service name:

```
Service: api        → EVE_APP_API_URL_API
Service: analytics  → EVE_APP_API_URL_ANALYTICS
Service: my-svc     → EVE_APP_API_URL_MY_SVC
```

Rule: uppercase, replace non-alphanumeric with `_`.

## Distribution Modes

### Repo-Bundled (Primary)

The CLI lives in the app repo as a pre-bundled single-file executable:

```
cli/
  src/index.ts         # Source
  bin/myapp            # Built artifact (esbuild bundle, committed to repo)
  package.json         # Build deps only
```

**How it works:**
1. Agent workspace clones the app repo (already happens)
2. Platform reads manifest, finds `x-eve.cli` with `bin: cli/bin/myapp`
3. Platform runs `chmod +x ${workspace}/cli/bin/myapp`
4. Platform symlinks to `/usr/local/bin/myapp`
5. Agent runs `myapp --help`

**Latency: zero** — the file is already present after clone.

**Build the bundle** (via `cli/build.mjs`):
```javascript
import { build } from 'esbuild';
import { readFile, writeFile, chmod } from 'node:fs/promises';

await build({
  entryPoints: ['cli/src/index.ts'],
  bundle: true, platform: 'node', target: 'node20',
  format: 'cjs',  // CJS — commander uses require() internally
  outfile: 'cli/bin/myapp',
});
const code = await readFile('cli/bin/myapp', 'utf8');
await writeFile('cli/bin/myapp', '#!/usr/bin/env node\n' + code);
await chmod('cli/bin/myapp', 0o755);
```

Use `format: 'cjs'` — commander and other Node libs use `require()`. Do NOT set `"type": "module"` in `package.json`.

Commit `cli/bin/myapp` to the repo. It's a build artifact (~50-200KB), small enough to version.

### Image-Based (Compiled CLIs)

For Go, Rust, or other compiled binaries:

```dockerfile
# Dockerfile.cli
FROM rust:1.77 AS build
COPY . .
RUN cargo build --release

FROM busybox:stable
COPY --from=build /app/target/release/myapp /cli/bin/myapp
```

**How it works:**
1. Platform adds an init container pulling the CLI image
2. Init container copies `/cli/bin/myapp` to shared volume at `/opt/eve/app-cli/myapp/bin/`
3. `EVE_APP_CLI_PATHS` env var set, entrypoint extends PATH
4. Agent runs `myapp --help`

**Latency: 2-5s** (image pull, cached after first run). Same pattern as toolchains.

**Critical:** Use `busybox:stable` as the final image stage, not `FROM scratch`. Init containers need `sh` and `cp` to function.

## CLI Implementation Pattern

### API Client Module

```typescript
// cli/src/client.ts
const SERVICE = 'API'; // matches manifest service name, uppercased

export function getApiUrl(): string {
  const url = process.env[`EVE_APP_API_URL_${SERVICE}`];
  if (!url) {
    console.error(`Error: EVE_APP_API_URL_${SERVICE} not set.`);
    console.error('Run inside an Eve job with: with_apis: [api]');
    process.exit(1);
  }
  return url;
}

export async function api<T = unknown>(
  method: string,
  path: string,
  body?: unknown,
): Promise<T> {
  const url = getApiUrl();
  const token = process.env.EVE_JOB_TOKEN;
  const res = await fetch(`${url}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({} as Record<string, string>));
    console.error(`${method} ${path} → ${res.status}: ${err.message || res.statusText}`);
    process.exit(1);
  }
  return res.json() as Promise<T>;
}
```

### Command Entry Point

```typescript
// cli/src/index.ts
import { Command } from 'commander';
import { api } from './client.js';
import { readFile } from 'node:fs/promises';

const program = new Command();
program.name('myapp').description('My App CLI').version('1.0.0');

// Subcommand group
const items = program.command('items').description('Manage items');

items.command('list')
  .description('List all items')
  .option('--json', 'JSON output')
  .action(async (opts) => {
    const data = await api('GET', '/items');
    if (opts.json) return console.log(JSON.stringify(data, null, 2));
    for (const item of data) console.log(`${item.id}  ${item.name}`);
  });

items.command('create')
  .description('Create an item from JSON file')
  .requiredOption('--file <path>', 'JSON file with item data')
  .action(async (opts) => {
    const body = JSON.parse(await readFile(opts.file, 'utf8'));
    const result = await api('POST', '/items', body);
    console.log(`Created: ${result.id}`);
  });

items.command('delete')
  .description('Delete an item')
  .argument('<id>', 'Item ID')
  .action(async (id) => {
    await api('DELETE', `/items/${id}`);
    console.log(`Deleted: ${id}`);
  });

program.parse();
```

### Auto-Detection Pattern

When only one resource exists, detect automatically:

```typescript
export async function autoDetectProject(): Promise<string> {
  const projects = await api<Array<{ id: string; name: string }>>('GET', '/projects');
  if (projects.length === 1) return projects[0].id;
  if (projects.length === 0) {
    console.error('No projects found.');
    process.exit(1);
  }
  console.error('Multiple projects found. Use --project <id>:');
  for (const p of projects) console.error(`  ${p.id}  ${p.name}`);
  process.exit(1);
}
```

Use in commands:
```typescript
program.command('map')
  .argument('[project-id]', 'Project ID (auto-detected if only one)')
  .option('--json', 'JSON output')
  .action(async (projectId, opts) => {
    const pid = projectId || await autoDetectProject();
    const map = await api('GET', `/projects/${pid}/map`);
    if (opts.json) return console.log(JSON.stringify(map, null, 2));
    printMap(map);
  });
```

## Output Conventions

All commands follow these rules:

| Mode | Behavior |
|------|----------|
| Default | Human-readable: tables, summaries, one-line confirmations |
| `--json` | Machine-readable JSON on stdout |
| Errors | stderr, exit code 1, actionable message with context |

**Examples:**
```bash
$ myapp items list
ID          NAME              STATUS
item_abc    Widget Alpha      active
item_def    Widget Beta       draft

$ myapp items list --json
[{"id":"item_abc","name":"Widget Alpha","status":"active"},...]

$ myapp items delete item_missing
items delete item_missing → 404: Item not found

$ echo $?
1
```

## Agent Integration

### Auto-Discovery (Zero Config)

The platform automatically scans the manifest for services with `x-eve.cli` or `x-eve.api_spec` declarations. Every agent job in the project gets those CLIs on PATH — no explicit `with_apis` needed. Just declare the CLI in the manifest and all agents see it.

### Explicit `with_apis` (Optional)

Use `with_apis` to restrict which APIs a specific agent or workflow step sees. When provided, it overrides auto-discovery:

```yaml
# agents.yaml
agents:
  my-agent:
    skill: my-skill
    with_apis:
      - service: api          # explicit: only this service
```

### Agent Instruction Block

When app APIs are resolved (via auto-discovery or explicit `with_apis`) and a service has a CLI, the instruction block tells the agent:

```
**Available App APIs** (env vars injected by platform):
- **api** (openapi): `http://api.svc.cluster.local:3000`
  - CLI: `myapp` (on PATH — run `myapp --help` to see commands)
  - Fallback: `curl "$EVE_APP_API_URL_API/..." -H "Authorization: Bearer $EVE_JOB_TOKEN"`
```

### Skill File Pattern

Agent skill files should reference the CLI:

```markdown
## API Access

Use the `eden` CLI for all API interactions:

​```bash
eden projects list --json
eden map show --project auto
eden changeset create --project $PID --file /tmp/changes.json
eden changeset accept $CHANGESET_ID
​```

Run `eden --help` for the full command reference.
```

## Testing

### Local Testing

```bash
# Set env vars manually
export EVE_APP_API_URL_API=http://localhost:3000
export EVE_JOB_TOKEN=$(eve auth token)

# Run commands
./cli/bin/myapp items list
./cli/bin/myapp items create --file test.json
```

### CI Testing

```bash
# Build the bundle
npm run build:cli

# Verify it runs
./cli/bin/myapp --help
./cli/bin/myapp --version
```

### Integration Testing

```bash
# Start the app
docker-compose up -d

# Test against running API
EVE_APP_API_URL_API=http://localhost:3000 ./cli/bin/myapp items list
```

## Platform Setup Flow (Internal)

For platform developers implementing CLI support:

```
1. Manifest sync → store cli metadata alongside api_spec
2. Job creation with --with-apis → resolveAppApis() includes cli info
3. Instruction block enhanced: "CLI: myapp (run myapp --help)"
4. Workspace setup (after clone):
   a. Parse manifest from workspace
   b. For each service with x-eve.cli:
      - Repo mode: chmod +x, symlink to /usr/local/bin
      - Image mode: add init container (same as toolchains)
5. Agent starts with CLI on PATH and env vars set
```

## Comparison

| Dimension | App CLI | `eve api call` | Raw curl |
|-----------|---------|----------------|----------|
| Auth handling | Invisible | Automatic | Manual |
| URL construction | None | Need path | Full URL |
| JSON payloads | `--file` flag | `--json` flag | Shell quoting |
| Error messages | Domain-specific | HTTP status | HTTP status |
| Discoverability | `--help` | `eve api spec` | Read docs |
| LLM calls per op | 1 | 1-2 | 3-5 |
