# OpenClaw Session Compact - QWEN Context

## Project Overview

**OpenClaw Session Compact** is a TypeScript-based plugin for the OpenClaw AI assistant framework. It provides **intelligent session compression** to manage token consumption and enable unlimited-length conversations.

When a conversation approaches the model's token limit, the plugin automatically compresses historical messages into structured summaries, achieving **85-95% token savings** while preserving key context (timeline, todos, files, tools used).

## Key Details

| Attribute | Value |
|-----------|-------|
| **Name** | `openclaw-session-compact` |
| **Version** | 1.0.0 |
| **Type** | OpenClaw Plugin (npm package) |
| **Language** | TypeScript (ESM) |
| **License** | MIT |
| **Entry Point** | `dist/index.js` |

## Architecture

### Core Modules

| File | Purpose |
|------|---------|
| `src/index.ts` | Plugin entry point — exports `register()` function with CLI registration |
| `src/compact/config.ts` | Configuration management with defaults (`max_tokens: 10000`, `preserve_recent: 4`) |
| `src/compact/engine.ts` | Core compression logic — token estimation, summary generation, session compaction |
| `src/cli/register.ts` | Legacy CLI command registration (used by bin script) |
| `bin/openclaw-compact.js` | Standalone CLI entry point (for direct execution) |

### Key Functions

- **`estimateTokenCount(messages)`** — Simplified token estimation (~4 chars ≈ 1 token)
- **`shouldCompact(messages, config)`** — Checks if total tokens exceed 90% of threshold
- **`generateSummary(messages, config)`** — Calls OpenClaw LLM via CLI to produce structured summary
- **`compactSession(messages, config)`** — Main compression entry point, returns `CompactionResult`
- **`extractTimelineFromMessages(messages)`** — Code-based timeline extraction (LLM-independent fallback)
- **`mergeCompactedSummaries(old, new)`** — Merges summaries across multiple compression cycles

### Plugin Registration

The plugin uses `api.registerCli()` to register CLI commands with OpenClaw:

```typescript
export function register(api: any) {
  api.registerCli(
    async ({ program }) => {
      program.command('compact').action(...)
      program.command('compact-status').action(...)
      program.command('compact-config').action(...)
    },
    {
      commands: ['compact', 'compact-status', 'compact-config'],
      descriptors: [...]
    }
  );
}
```

### Compression Flow

1. Monitor token usage per session
2. When >90% of `max_tokens` threshold → trigger compression
3. Keep last N messages (`preserve_recent`, default 4)
4. Compress older messages via LLM-generated structured summary (with code-based fallback)
5. Replace old messages with summary, continue conversation seamlessly

## Building and Running

```bash
# Install dependencies
npm install

# Build (compile TypeScript to dist/)
npm run build

# Development mode (watch for changes)
npm run dev

# Run tests
npm test

# Check test coverage
npm run test:coverage

# Clean build artifacts
npm run clean
```

## Plugin Installation

The plugin is installed as an OpenClaw extension:

**Location**: `~/.openclaw/extensions/openclaw-session-compact/`

**Required files**:
- `package.json` with `"openclaw": { "extensions": ["./dist/index.js"] }`
- `openclaw.plugin.json` with `id`, `cli`, and `configSchema`
- `dist/index.js` with `export function register(api)`
- `dist/` compiled output

**Config** (`~/.openclaw/openclaw.json`):
```json
{
  "plugins": {
    "allow": ["openclaw-session-compact"],
    "entries": {
      "openclaw-session-compact": { "enabled": true }
    }
  }
}
```

## CLI Commands

```bash
# Check session status
openclaw compact-status

# Manual compression
openclaw compact

# Force compression (ignores threshold)
openclaw compact --force

# View/edit configuration
openclaw compact-config
openclaw compact-config max_tokens
openclaw compact-config max_tokens 5000
```

## Development Conventions

- **TypeScript strict mode** enabled (`tsconfig.json`)
- **ESM modules** (`"type": "module"`, `NodeNext` module resolution)
- **Target**: ES2022
- **Testing**: Jest with ts-jest preset, ESM support enabled
- **Test location**: `src/compact/__tests__/*.test.ts`
- **Current coverage**: ~63.63% (target: 70%+)
- **65 unit tests** passing

## Configuration

Plugin config via `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "openclaw-session-compact": {
        "enabled": true,
        "max_tokens": 10000,
        "preserve_recent": 4,
        "auto_compact": true,
        "model": "qwen/qwen3.5-122b-a10b"
      }
    }
  }
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_tokens` | number | 10000 | Token threshold for compression |
| `preserve_recent` | number | 4 | Number of recent messages to keep |
| `auto_compact` | boolean | true | Enable automatic compression |
| `model` | string | '' | Model for summary generation (empty = use global default) |

## Dependencies

| Package | Type | Version |
|---------|------|---------|
| `commander` | runtime | ^12.0.0 |
| `typescript` | dev | ^5.3.0 |
| `jest` | dev | ^29.7.0 |
| `ts-jest` | dev | ^29.1.0 |
| `@types/node` | dev | ^20.10.0 |
| `openclaw` | peer | ^2026.3.28 |

## Known Limitations / TODOs

- **Session retrieval**: `getCurrentSessionMessages()` uses mock data — needs integration with actual OpenClaw session storage
- **LLM integration**: `callLLM()` invokes OpenClaw CLI via `execSync` — works but could be optimized with direct API calls
- **Test coverage**: Below 70% target
- **No unit tests** for CLI registration in `src/index.ts`
- **Workspace skill**: The `SKILL.md` in `workspace/skills/` is recognized by OpenClaw as a documentation skill but the actual compression logic runs via the plugin system

## Project Structure

```
openclaw-session-compact/
├── src/
│   ├── index.ts              # Plugin register() + CLI via api.registerCli()
│   ├── compact/
│   │   ├── config.ts         # Config types and defaults
│   │   ├── engine.ts         # Core: token estimation, summary, compaction
│   │   └── __tests__/        # 65 unit tests
│   └── cli/
│       └── register.ts       # Legacy CLI registration (for bin script)
├── bin/
│   └── openclaw-compact.js   # Standalone CLI entry point
├── dist/                     # Compiled JS output
├── package.json
├── openclaw.plugin.json      # OpenClaw plugin manifest
├── tsconfig.json
├── SKILL.md                  # Skill documentation (with YAML frontmatter)
├── SKILL_CN.md              # Chinese documentation
├── README.md                 # Full documentation
└── node_modules/
```

## Key Learnings

### OpenClaw Plugin System
1. **Plugin discovery**: Scans `~/.openclaw/extensions/` for directories with `package.json` containing `"openclaw": { "extensions": [...] }`
2. **Plugin manifest**: `openclaw.plugin.json` requires `id`, `cli` (command names), and `configSchema`
3. **Plugin entry**: Must export `register(api)` function
4. **CLI registration**: Use `api.registerCli(registrar, { commands, descriptors })` — NOT `api.registerCommand()`
5. **Plugin allowlist**: Plugin ID must be in `plugins.allow` in `openclaw.json`

### OpenClaw Skill System (separate from plugins)
1. **Workspace skills**: `workspace/skills/` directories with `SKILL.md` files
2. **SKILL.md frontmatter**: Requires YAML frontmatter with `name` and `description` fields
3. **Skills are documentation-only**: No code execution, just prompts for the LLM
