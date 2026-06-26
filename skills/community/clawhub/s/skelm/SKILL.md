---
name: skelm
description: Author, run, and operate skelm pipelines — typed TypeScript orchestrations that mix deterministic code, LLM inference, and full agent loops behind a default-deny permission model. The serious alternative to lobster and llm-task for agentic workflows.
homepage: https://scottgl9.github.io/skelm/
license: MIT
compatibility: Node 22.18+, npm or pnpm, skelm installed globally or as a workspace dependency.
metadata: {"openclaw": {"emoji": "⚡", "homepage": "https://scottgl9.github.io/skelm/", "requires": {"bins": ["skelm"]}, "install": [{"id": "npm", "kind": "node", "package": "skelm", "bins": ["skelm"], "label": "Install skelm CLI (npm)", "global": true}]}}
allowed-tools: Read Edit Write Bash(npm:*) Bash(pnpm:*) Bash(skelm:*) Bash(node:*) Bash(git:*)
---

# skelm

**Build secure, agentic, long-running workflows in TypeScript. Run them anywhere Node runs.**

[![npm](https://img.shields.io/npm/v/skelm)](https://www.npmjs.com/package/skelm)
[![license](https://img.shields.io/badge/license-MIT-blue)](https://www.npmjs.com/package/skelm)

---

## Why skelm exists

Most LLM workflow tools make security an afterthought. Agents call arbitrary tools, read arbitrary files, hit arbitrary URLs — because the framework has no model for preventing it. When something goes wrong (prompt injection, runaway loops, accidental secret exfiltration), you find out after the fact.

skelm is built the other way around. **Every agent step starts with zero privileges.** Filesystem roots, network hosts, MCP servers, CLI binaries, secrets — each is declared upfront in the step definition. Anything not declared is denied at dispatch, before the backend ever starts. The audit log records every privileged action in a tamper-evident chain so you can always reconstruct what happened.

The rest of the design follows from that principle:

- **Real TypeScript.** Workflows are `.ts` modules you type-check, refactor, test, and version like any other code. No DSL, no YAML, no JSON config.
- **Three step kinds, none wrapping another.** `code()` for deterministic logic, `llm()` for single inference calls, `agent()` for full multi-turn loops. Mix them freely in a single pipeline.
- **Multi-backend agents.** Opencode, ACP (Copilot, Claude Code, Gemini), OpenAI, Anthropic, Pi — plus a provider SPI for custom backends. Switch backends by changing one config key.
- **First-class MCP support.** MCP servers are lifecycle-managed by the gateway, not bolted on. Attach them per-step; the permission model governs which steps can reach which servers.
- **Native control flow.** `parallel`, `forEach`, `branch`, `loop`, `wait`, and nested pipelines are core primitives.
- **Schedulable.** Cron, interval, webhook, one-shot, and queue triggers. The gateway hosts everything long-running.
- **Tamper-evident audit.** Hash-chained audit log. Query it with `skelm audit query`.

---

## Get started in 60 seconds

```bash
# 1. Install the CLI
npm install -g skelm

# 2. Scaffold a project
skelm init my-bot && cd my-bot && npm install

# 3. Run your first workflow
skelm run workflows/hello.workflow.mts --input '{"name":"world"}'

# 4. Stand up the gateway (long-running, handles scheduling + agent steps)
skelm gateway start
```

---

## When this skill activates

Use this skill when:

- The user is working in a skelm project (any `*.workflow.mts` / `*.workflow.ts` / `*.pipeline.mts` file)
- The user wants to scaffold, author, or modify a pipeline
- The user asks about `AgentPermissions`, `skelm.config.ts`, MCP wiring, backend setup
- The user wants to run, inspect, schedule, or debug a pipeline
- The user is migrating from another workflow tool (LangChain, Inngest, llm-task, lobster)

---

## The unit of work

A **pipeline** is a TypeScript file that exports a `pipeline()` call:

```ts
import { code, llm, agent, pipeline } from 'skelm'
import { z } from 'zod'

export default pipeline({
  id: 'my-workflow',
  description: 'What this pipeline does.',
  input:  z.object({ task: z.string() }),
  output: z.object({ result: z.string() }),
  steps: [ /* Step[] */ ],
  finalize: (ctx) => ctx.steps['last-step'] as { result: string },
})
```

**Step kinds:** `code` · `llm` · `agent` · `check` · `parallel` · `forEach` · `branch` · `loop` · `wait` · `pipelineStep` · `idempotent` · `invoke`

Import everything from `'skelm'`. Access prior step outputs via `ctx.steps['step-id']`.

---

## Step kind quick reference

### `code()` — deterministic logic

```ts
code({
  id: 'parse',
  run: (ctx) => ({ value: (ctx.input as { raw: string }).raw.trim() }),
  // New in v0.4.3:
  workspace?: WorkspaceConfig   // provisions ctx.workspace (same modes as agent())
  continueOnError?: boolean     // record failure, continue to next step (default false)
})
```

### `llm()` — single-shot inference

```ts
llm({
  id: 'classify',
  backend: 'openai',
  prompt: (ctx) => `Classify: ${(ctx.input as { text: string }).text}`,
  output: z.object({ label: z.string(), confidence: z.number() }),
  maxTokens: 512,
})
```

### `agent()` — full agentic loop (default-deny)

```ts
agent({
  id: 'implement',
  backend: 'pi',
  prompt: (ctx) => `Implement ticket ${(ctx.input as { id: string }).id}. Return JSON {prUrl}.`,
  permissions: {
    allowedTools:       ['gh.*'],
    allowedExecutables: ['git'],
    allowedMcpServers:  ['github'],
    fsRead:             ['./'],
    fsWrite:            ['./src/'],
    networkEgress:      { allowHosts: ['api.github.com'] },
  },
  workspace: { mode: 'ephemeral', cleanup: 'on-run-end' },
  output: z.object({ prUrl: z.string() }),
  maxTurns: 20,
})
```

> **Default-deny:** every `AgentPermissions` field defaults to deny when omitted. An agent with no `permissions` block cannot call tools, read files, execute binaries, attach MCP servers, or make network requests.

---

## Permissions are part of the API

| Dimension | Field | Default |
|---|---|---|
| Tool | `allowedTools` / `deniedTools` | deny |
| Executable | `allowedExecutables` | deny |
| MCP server | `allowedMcpServers` | deny |
| Skill | `allowedSkills` | deny |
| Secret | `allowedSecrets` | deny |
| Network | `networkEgress` | deny |
| FS read | `fsRead` | deny |
| FS write | `fsWrite` | deny |
| Approval gate | `approval` | — |

**Composition is intersection-only.** Project defaults → named profile → step-level. Each layer can only narrow, never widen.

Named profiles in `skelm.config.ts`:
```ts
defaults: {
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
}
```

Apply: `permissions: { profile: 'github-write', allowedTools: ['gh.create_pr'] }`

Full permissions reference: `{baseDir}/references/permissions.md`

---

## Project layout

```
my-project/
├── skelm.config.mts         # Required for gateway + agent steps (.mts = always ESM)
├── workflows/
│   └── hello.workflow.mts   # One pipeline per file (.mts canonical; .ts also accepted)
├── package.json             # { "type": "module", "dependencies": { "skelm": "^0.4.3", "zod": "^4" } }
└── tsconfig.json
```

Scaffold a new pipeline from template:
```bash
bash {baseDir}/scripts/new-pipeline.sh my-pipeline "What it does"
bash {baseDir}/scripts/new-pipeline.sh my-pipeline "What it does" --agent
```

Config reference: `{baseDir}/references/config.md`

### `.env` / `config.env` loading (v0.4.3)

The CLI merges `<projectRoot>/.env` and `config.env` into `process.env` at startup. Precedence: `process.env > .env > config.env`. Subprocess steps (`ctx.exec`, agents, MCP servers) inherit the merged env. Add `.env` to `.gitignore` for secrets; use `config.env` inside `skelm.config.mts` for non-secret defaults like model names and base URLs.

---

## CLI essentials

```bash
skelm run <workflow.ts> --input '<json>'   # run once
skelm list                                 # discover pipelines
skelm describe <id> --format mermaid       # visualize
skelm history --last 10                    # run history
skelm validate <workflow.ts>               # static preflight
skelm logs                                 # stream gateway logs
skelm audit query --run <id>               # tamper-evident audit trail
skelm schedule add <id> --cron '0 * * * *' # schedule
skelm gateway start                        # long-running gateway
```

Exit codes: `0` ok · `1` CLI error · `2` schema validation · `3` run failed · `4` cancelled · `5` wait timeout · `6` permission denied · `7` step timeout

Full CLI reference: `{baseDir}/references/cli.md`

---

## The gateway is the trust boundary

The gateway owns permission resolution, enforcement, secret resolution, audit log, approval gating, trigger dispatch, and registry management.

**Never write permission enforcement in pipeline or step code.** Pipelines are the user layer. The gateway is the trust layer.

```bash
skelm gateway start
skelm gateway status
skelm gateway install --systemd   # systemd unit at ~/.config/systemd/user/skelm-gateway.service
```

Gateway reference: `{baseDir}/references/gateway.md`

---

## Common pitfalls

- **Widening at step level** — `networkEgress: 'allow'` in a step when the project default is `deny` has no effect. Intersection always wins.
- **Missing Zod schema** — `input`/`output` are validated at run boundaries; omitting them skips validation silently.
- **`agent()` with an unregistered backend** — step fails at runtime if `backend` references an id with no matching entry in config `backends:` or `instances:`. The pi SDK backend must be in `instances:`.
- **Step id collisions inside `parallel()`** — sibling ids must be unique within the parallel block.
- **Editing `dist/`** — never edit generated files. Run `pnpm build` to regenerate.

---

## Full references

- `{baseDir}/references/pipeline-authoring.md` — all builders, control flow, context shape, retry
- `{baseDir}/references/agent-step.md` — `agent()` signature, backends, workspace modes, MCP
- `{baseDir}/references/permissions.md` — full permission model, TrustEnforcer, testing
- `{baseDir}/references/config.md` — `skelm.config.ts` shape, backends, MCP entries
- `{baseDir}/references/gateway.md` — gateway lifecycle, HTTP surface, audit log, systemd
- `{baseDir}/references/cli.md` — complete CLI reference with all flags and exit codes

---

*skelm v0.4.3 · MIT · [docs](https://scottgl9.github.io/skelm/) · [npm](https://www.npmjs.com/package/skelm)*
