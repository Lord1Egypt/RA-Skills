# Config reference (`skelm.config.mts`)

The CLI walks up from `cwd` to find `skelm.config.mts` (tried first), then `.ts`, `.js`, `.mjs`. When none is found, the gateway uses [`DEFAULT_CONFIG`].

## Shape

```ts
import { defineConfig } from 'skelm'

export default defineConfig({
  // ── Backends ────────────────────────────────────────────────────────
  backend?: string,                          // legacy single-backend selector; prefer `backends.default`
  backends?: {
    default?: string,                        // used by both llm() and agent() unless overridden
    llm?:     string,                        // optional override for llm()
    agent?:   string,                        // optional override for agent()
    [id: string]: SkelmConfigBackendEntry | string | undefined,
  },
  /**
   * Pre-built `SkelmBackend` instances. Use this when the string-keyed
   * `backends:` form is insufficient — e.g. the pi SDK backend, custom
   * ACP backends, or a backend you wrote yourself.
   */
  instances?: readonly SkelmBackend[],

  // ── Workflow discovery ──────────────────────────────────────────────
  pipelines?: {
    discovery?: 'auto' | 'explicit',
    glob?:      string,                      // e.g. 'workflows/**/*.workflow.{mts,ts}'
    explicit?:  readonly string[],
  },

  // ── Gateway-managed registries ──────────────────────────────────────
  registries?: {
    workflows?:  { glob?: string },          // file-system discovery for *.workflow.{mts,ts} / *.pipeline.{mts,ts}
    skills?:     { glob?: string },          // skill SKILL.md directories
    mcpServers?: readonly SkelmConfigMcpServerEntry[],
    agents?:     readonly SkelmConfigAgentEntry[],   // gateway-supervised agent runtimes
  },

  // ── Defaults & profiles ─────────────────────────────────────────────
  defaults?: {
    backend?:            string,             // alias for backends.default
    permissions?:        AgentPermissions,   // project-wide permission baseline
    permissionProfiles?: Record<string, AgentPermissions>,
  },

  // ── Operational surfaces ────────────────────────────────────────────
  secrets?: {
    driver?: 'env' | 'file',
    file?:   string,                         // path to JSON secrets file when driver === 'file'
  },
  storage?: {
    runs?:       { driver?: 'sqlite' | 'memory', path?: string },
    state?:      { driver?: 'sqlite' | 'memory', path?: string },
    workspaces?: { base?: string, ephemeralBase?: string },
  },
  server?: {
    port?:              number,              // default: 14738
    host?:              string,              // default: 127.0.0.1
    auth?:              { mode: 'none' | 'bearer' },
    maxConcurrentRuns?: number,              // default: 10
  },
  plugins?: readonly string[],               // package names imported at gateway startup

  // ── Environment variables (v0.4.3) ─────────────────────────────────
  env?: Record<string, string>,              // static non-secret defaults; layered under .env
})
```

`SkelmConfigBackendEntry` is a free-form record forwarded to the matching factory. Strings allowed for keys like `backends.default` (selectors), record values for backend-specific config (`apiKey`, `model`, `baseUrl`, …).

## Backends

The CLI knows these ids and wires them automatically:

| id              | factory                                | notes                                  |
|-----------------|----------------------------------------|----------------------------------------|
| `openai`        | `createOpenAIBackend`                  | OpenAI-compatible HTTP endpoint        |
| `anthropic`     | `createAnthropicBackend`               | Direct Anthropic API                   |
| `opencode`      | `createOpencodeBackendFromConfig`      | opencode SDK                           |
| `copilot-acp`   | `createAcpBackend`                     | GitHub Copilot ACP subprocess          |
| `acp`           | `createAcpBackend`                     | Generic ACP; `command` required        |
| `pi`            | `createPiBackendFromConfig` (RPC)      | RPC variant only — for SDK use `instances:` |

For the **pi SDK** backend, register an instance:

```ts
import { defineConfig } from 'skelm'
import { createPiSdkBackend } from '@skelm/pi'

export default defineConfig({
  backends: { agent: 'pi' },
  instances: [createPiSdkBackend({ id: 'pi' })],
})
```

API keys can be inlined (`apiKey: 'sk-...'`) or resolved from env (`apiKey: { secret: 'OPENAI_API_KEY' }`). The runtime resolves the secret at gateway start.

## Agent registry entries

`registries.agents` declares agent runtimes the **gateway** supervises (process lifecycle, command, env). This is separate from the `backends:` map (which registers `SkelmBackend` instances directly).

```ts
interface SkelmConfigAgentEntry {
  id: string
  runtime: 'claude-code' | 'opencode' | 'pi' | 'acp' | string
  lifecycle: 'ephemeral' | 'resident'
  command?: string                    // spawn command for ephemeral, or `serve` for resident
  args?: readonly string[]
  url?: string                        // when the agent is reachable as a long-lived server
  env?: Readonly<Record<string, string>>
  permissions?: AgentPermissions      // applied to every step that uses this agent
  metadata?: Readonly<Record<string, unknown>>
}
```

- `ephemeral` — spawned per step, exits when done.
- `resident` — gateway keeps the process alive, reuses across steps.

## MCP server entries

```ts
interface SkelmConfigMcpServerEntry {
  id: string
  transport: 'stdio' | 'http' | 'sse'
  // stdio:
  command?: string
  args?: readonly string[]
  env?: Readonly<Record<string, string>>
  // http / sse:
  url?: string
}
```

## Full example

```ts
import { defineConfig } from 'skelm'
import { createPiSdkBackend } from '@skelm/pi'

export default defineConfig({
  backends: {
    default: 'openai',
    agent:   'pi',
    openai: {
      baseUrl: 'https://api.openai.com/v1',
      apiKey:  { secret: 'OPENAI_API_KEY' },
      model:   'gpt-4o-mini',
    },
  },
  instances: [createPiSdkBackend({ id: 'pi' })],

  pipelines: { discovery: 'auto', glob: 'workflows/**/*.workflow.ts' },

  registries: {
    workflows:  { glob: 'workflows/**/*.workflow.ts' },
    skills:     { glob: 'skills/**/SKILL.md' },
    mcpServers: [
      { id: 'github',     transport: 'http',  url: 'http://127.0.0.1:9100' },
      { id: 'filesystem', transport: 'stdio', command: 'mcp-server-filesystem', args: ['.'] },
    ],
  },

  defaults: {
    permissions: {
      allowedExecutables: [],
      allowedTools: [],
      allowedSkills: [],
      allowedMcpServers: [],
      fsRead: ['./'],
      fsWrite: [],
      networkEgress: 'deny',
    },
    permissionProfiles: {
      'github-write': {
        allowedExecutables: ['git'],
        allowedTools:       ['gh.*'],
        allowedMcpServers:  ['github'],
        fsRead:             ['./'],
        fsWrite:            ['./'],
        networkEgress:      { allowHosts: ['api.github.com'] },
      },
    },
  },

  secrets: { driver: 'env' },

  storage: {
    runs:  { driver: 'sqlite', path: '.skelm/runs.sqlite' },
    state: { driver: 'sqlite', path: '.skelm/state.sqlite' },
  },

  server: {
    port: 14738,
    host: '127.0.0.1',
    auth: { mode: 'none' },
  },
})
```

## Notes

- Config is hot-reloaded when the gateway receives `SIGHUP` or `skelm gateway reload`.
- `permissionProfiles` entries narrow `defaults.permissions`; profiles cannot widen the project baseline.
- When `registries.workflows.glob` is omitted, the gateway uses the value from `pipelines.glob` (or the default `workflows/**/*.workflow.{mts,ts}`).
- `secrets.driver: 'file'` reads JSON from `secrets.file`; the gateway never logs secret values.

## `.env` / `config.env` loading (v0.4.3)

At startup the CLI merges env into `process.env` with precedence `process.env > .env > config.env`:

1. `config.env` — static defaults inside `skelm.config.mts`
2. `<projectRoot>/.env` — dotenv file at config dir (gitignore this if it has secrets)
3. `process.env` — always wins

```ts
// skelm.config.mts
export default defineConfig({
  env: {
    OPENAI_MODEL: 'gpt-4o-mini',
    OPENAI_BASE_URL: 'https://api.openai.com/v1',
  },
})
```

Subprocess steps (`ctx.exec`, agents, MCP servers) inherit the merged env. Use `secrets.driver` for actual secrets.
