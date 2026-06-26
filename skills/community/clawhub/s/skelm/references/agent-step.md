# Agent step reference

## Full `agent()` signature

```ts
agent({
  id: string                                          // required
  backend?: string | readonly string[]                // backend id(s) — first match wins
  agentDef?: string                                   // path to a directory holding AGENTS.md / SOUL.md
  prompt: string | ((ctx: Context) => string)         // required
  system?: string | ((ctx: Context) => string)
  mcp?: McpServerConfig[] | ((ctx: Context) => McpServerConfig[])
  skills?: readonly string[]                          // skill ids the agent should load
  secrets?: readonly string[]                         // secret names resolved before the run
  workspace?: WorkspaceConfig | ((ctx: Context) => WorkspaceConfig)
  output?: SkelmSchema<TOutput>                       // validates agent's final output
  permissions?: AgentPermissions                      // default-deny; all fields optional
  maxTurns?: number                                   // cap on agent tool-call turns
  timeoutMs?: number                                  // wall-clock cap; positive integer
  state?: StateConfig
  retry?: RetryPolicy
})
```

## Backends

Two ways to register a backend:

1. **`backends:` map** — string-keyed; the CLI wires the standard factories from your config.
   ```ts
   // skelm.config.mts
   import { defineConfig } from 'skelm'

   export default defineConfig({
     backends: {
       default: 'openai',
       opencode: { apiKey: { secret: 'OPENCODE_API_KEY' }, agent: 'build' },
     },
   })
   ```
2. **`instances:` array** — pre-built `SkelmBackend` values. Use this for the pi SDK backend or any custom backend.
   ```ts
   import { defineConfig } from 'skelm'
   import { createPiSdkBackend } from '@skelm/pi'

   export default defineConfig({
     backends: { agent: 'pi' },
     instances: [createPiSdkBackend({ id: 'pi' })],
   })
   ```

Reference by id at the step level:

```ts
agent({ id: 'implement', backend: 'pi', prompt: '...' })
```

If `backend` is omitted on the step, the runtime resolves it from (in order): `config.backends.agent`, `config.backends.default`, `config.backend`, `config.defaults.backend`. If none of those is set the step fails at start.

### Pi backends (`@skelm/pi`)

Two pi backends ship in `@skelm/pi`. Prefer the **SDK** backend — it gives you native enforcement of the skelm permission policy and supports both `agent()` and `llm()` steps.

| | `createPiBackend` (RPC) | `createPiSdkBackend` (SDK) |
|---|---|---|
| Tool enforcement | Advisory | **Native** — pi hard-enforces the allowlist |
| `llm()` support  | No                      | Yes                          |
| System prompt    | Not controllable        | Pi's default; `req.system` appended; optional full replace |
| Peer dep         | `pi` CLI on `$PATH`     | `@mariozechner/pi-coding-agent` npm package |

Wiring:

```ts
import { defineConfig } from 'skelm'
import { createPiSdkBackend } from '@skelm/pi'

export default defineConfig({
  backends: { agent: 'pi' },
  instances: [
    createPiSdkBackend({ id: 'pi', maxConcurrent: 4 }),
  ],
})
```

The SDK backend defaults to `noExtensions: true` and `noSkills: true` so project-local pi extensions and skills don't expand the tool surface or duplicate skelm's skill injection. `noContextFiles: false` (default) keeps `AGENTS.md` and `.pi/context/` loaded.

Permission → pi tool mapping:
- `allowedExecutables` has `bash`/`sh` → `bash`
- `fsRead` non-empty → `read`, `grep`, `find`, `ls`
- `fsWrite` non-empty → `write`, `edit` (+ read tools)
- `networkEgress: 'deny'` → drops `bash` (pi has no native fetch tool, so removing shell is the only way to deny network)

⚠ **Permission semantics with the SDK backend differ from MCP-host backends.** Pi has one `bash` tool (not per-binary) — granting `bash` lets the agent run any executable. Filesystem paths are advisory: `fsRead`/`fsWrite` unlock the tool *category* but don't constrain paths. Use the SDK backend inside an already-bounded workspace (ephemeral cwd, OS sandbox, container); use MCP-host backends (opencode) when you need per-call binary/path enforcement.

## MCP servers

Attach MCP servers declared in `skelm.config.mts`:

```ts
// skelm.config.mts
registries: {
  mcpServers: [
    { id: 'github',     transport: 'http',  url: 'http://127.0.0.1:9100' },
    { id: 'filesystem', transport: 'stdio', command: 'mcp-server-filesystem', args: ['.'] },
  ],
}
```

In a step, the server must be both attached (`mcp:`) **and** allowed (`permissions.allowedMcpServers:`):

```ts
agent({
  id: 'research',
  backend: 'pi',
  prompt: 'Investigate the issue.',
  permissions: { allowedMcpServers: ['github'] },
  mcp: [{ id: 'github' }],
})
```

A server attached via `mcp:` but absent from `allowedMcpServers` is denied at dispatch.

## Workspace modes

### `ephemeral` — temporary directory, auto-cleaned

```ts
workspace: {
  mode: 'ephemeral',
  prefix?: string,                                       // directory prefix
  cleanup?: 'on-step-end' | 'on-run-end' | 'on-success', // default: 'on-run-end'
  seed?: { copy: readonly string[] },                    // paths copied in before step starts
}
```

### `persistent` — named, git-aware, survives restarts

```ts
workspace: {
  mode: 'persistent',
  name: string,                        // workspace name; unique per pipeline id
  base?: string,                       // base directory
  gitRoot?: boolean,                   // initialize a git repo in the workspace
  cleanup?: 'never' | 'on-success',    // default: 'never'
  seed?: { copy: readonly string[] },
}
```

### `mounted` — user-supplied path

```ts
workspace: {
  mode: 'mounted',
  path: string,                        // absolute or cwd-relative path
  seed?: { copy: readonly string[] },
}
```

The workspace path becomes the agent's cwd; coding agents read/write source files there.

### `git-repo` — clone from GitHub (v0.4.2)

```ts
workspace: {
  mode: 'git-repo',
  repo: 'owner/name',              // or full git URL
  ref: 'main',                     // branch, tag, or SHA
  baseRef?: string,                // optional base ref (for PR diffs)
  cacheDir?: string,               // cache clone at this path; re-uses on subsequent runs
  auth?: { env: string },          // env var name holding a GITHUB_TOKEN
  seed?: { copy: readonly string[] },
}
```

The runner clones (or `git fetch`s) the repo and checks out `ref` before the step runs. `auth.env` value is passed via `http.extraheader` — never in `git remote -v`.

## Seed files

```ts
workspace: {
  mode: 'ephemeral',
  seed: { copy: ['./src/', './package.json', './tsconfig.json'] },
}
```

Paths are resolved relative to `process.cwd()` when the step executes.

## Full example

```ts
import { agent, pipeline } from 'skelm'
import { z } from 'zod'

export default pipeline({
  id: 'ticket-to-pr',
  description: 'Implements a ticket and opens a PR.',
  input: z.object({ ticketId: z.string(), description: z.string() }),
  output: z.object({ prUrl: z.string() }),
  steps: [
    agent({
      id: 'implement',
      backend: 'pi',
      prompt: (ctx) => {
        const { ticketId, description } = ctx.input as { ticketId: string; description: string }
        return `Implement ticket ${ticketId}: ${description}. Open a PR when done. Return JSON {prUrl}.`
      },
      permissions: {
        profile: 'github-write',                              // from skelm.config.mts profiles
        allowedTools:       ['gh.list_issues', 'gh.create_pr'],
        allowedExecutables: ['git', 'bash'],
        allowedMcpServers:  ['github'],
        allowedSkills:      [],
        fsRead:             ['./'],
        fsWrite:            ['./src/'],
        networkEgress:      { allowHosts: ['api.github.com'] },
      },
      workspace: {
        mode: 'ephemeral',
        seed: { copy: ['./src/', './package.json', './tsconfig.json'] },
        cleanup: 'on-run-end',
      },
      maxTurns: 50,
      output: z.object({ prUrl: z.string() }),
    }),
  ],
})
```
