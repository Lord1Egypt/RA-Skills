# Agent Guidelines for Session Memory Skill

This is an OpenClaw skill that provides automatic conversation memory loading and AI summarization during session compaction.

## Project Structure

```
session-context/
├── SKILL.md                    # Main skill documentation
├── _meta.json                  # Skill metadata (slug, hooks, version)
├── hooks/
│   └── session/
│       ├── start/handler.js     # Loads memory into new sessions
│       └── compact:before/     # Generates summaries before compaction
├── memory/                     # Auto-created; stores daily summaries
└── assets/                     # Templates and resources
```

## Build/Lint/Test Commands

This is a hook-based skill with no build system. Handlers are plain JavaScript/TypeScript executed directly by OpenClaw.

- **No build step required** - Handlers run directly
- **No linting configured** - Write clean ES module code
- **No tests** - Manual testing via OpenClaw hooks

### Manual Testing

1. Enable the skill: `openclaw skills enable session-context`
2. Start a new session to trigger `session:start` hook
3. Check `memory/` directory for generated files
4. Monitor logs for hook execution: `openclaw logs`

## Code Style Guidelines

### General Principles

- Write defensive code with early returns for guard clauses
- Always validate event/context structure before accessing properties
- Use `log.debug()` for flow tracing, `log.info()` for significant events
- Handle errors gracefully - hooks should not crash the session

### JavaScript Handlers

```javascript
import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';

export default async function (context) {
  const { workspace = process.cwd(), log = console } = context;
  
  if (!shouldProceed(context)) {
    return;
  }
  
  try {
    const result = await doSomething(context);
    log.info('Operation completed', { result });
  } catch (error) {
    log.error('Operation failed:', error);
  }
}
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | camelCase | `shouldSummarize`, `writeMemoryFile` |
| Variables | camelCase | `memoryDir`, `latestFile`, `tokenCount` |
| Constants | UPPER_SNAKE | `MAX_TOKENS`, `DEFAULT_THRESHOLD` |
| Types/Interfaces | PascalCase | `HookHandler`, `SessionContext` |
| Files | kebab-case | `session-start`, `compact-before` |

### Imports

```javascript
// Node.js built-ins
import { readFile, writeFile, mkdir } from 'fs/promises';
import { join, basename } from 'path';

// ES modules - no default exports for utilities
// Handlers always use default export
export default async function handler(context) { ... }
```

### Error Handling

```javascript
// For optional operations - catch and continue
const files = await readdir(memoryDir).catch(() => []);

// For required operations - try/catch with logging
try {
  const content = await readFile(filePath, 'utf8');
} catch {
  // File doesn't exist, create it
}

// Always include context in error logs
log.error('Hook failed:', { hook: 'session:start', error });
```

### Type Safety

```javascript
// Always validate before property access
if (!event || typeof event !== 'object') return;
if (!Array.isArray(event.context.bootstrapFiles)) return;

// Use optional chaining for deep access
const tokenCount = context.session?.tokenCount || 0;
const maxTokens = context.config?.maxTokens || 128000;
```

### Hook Handler Patterns

```javascript
export default async function (context) {
  const log = context.log || console;
  const workspace = context.workspace || process.cwd();
  
  if (!shouldRun(context)) return;
  
  // ... implementation
}
```

### File Operations

```javascript
// Always specify encoding
const content = await readFile(path, 'utf8');

// Use recursive option for mkdir
await mkdir(dir, { recursive: true });

// Write with explicit encoding
await writeFile(path, content, 'utf8');
```

### Context Access Patterns

```javascript
// Session context
const messages = context.messages || [];
const sessionEntry = context.sessionEntry;
const sessionEntry.messages?.unshift(newMessage);

// Config with defaults
const maxTokens = context.config?.maxTokens || 128000;
const threshold = context.config?.threshold || 0.6;
```

## OpenClaw Hooks Reference

### Available Hooks in This Skill

| Hook | Purpose | Handler |
|------|---------|---------|
| `session:start` | Load memory into new sessions | `hooks/session/start/handler.js` |
| `session:compact:before` | Generate summary before compaction | `hooks/session/compact:before/handler.js` |

### Hook Context Properties

- `context.workspace` - Current workspace directory
- `context.log` - Logger with `.debug()`, `.info()`, `.warn()`, `.error()`
- `context.messages` - Array of conversation messages
- `context.session` - Session metadata (tokenCount, etc.)
- `context.sessionEntry` - Session entry with messages array
- `context.config` - Configuration values

## Common Patterns

### Finding Most Recent File

```javascript
const files = await readdir(dir)
  .then(files => files.filter(f => f.endsWith('.md')));
files.sort((a, b) => b.localeCompare(a)); // Descending by name
const latest = join(dir, files[0]);
```

### Conditional Execution

```javascript
function shouldSummarize(context) {
  const msgCount = context.messages?.length || 0;
  const tokenCount = context.session?.tokenCount || 0;
  const maxTokens = context.config?.maxTokens || 128000;
  
  return msgCount >= 20 || tokenCount > maxTokens * 0.6;
}
```

### Prepending to File

```javascript
const existing = await readFile(path, 'utf8').catch(() => '');
const separator = existing ? '\n---\n' : '';
const content = newEntry + separator + existing;
await writeFile(path, content, 'utf8');
```

## What NOT To Do

- Don't modify `memory/` files during `session:start` (read-only)
- Don't crash on missing files - handle gracefully
- Don't use `console.log` - use `context.log` or `console` with fallback
- Don't assume properties exist - always validate with optional chaining
- Don't block the hook - use async/await, don't use sync fs in tight loops
