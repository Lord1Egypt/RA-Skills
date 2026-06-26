# Hook setup

Use this only if you want the ledger rebuilt automatically.

## Goal

Rebuild the ledger after these OpenClaw events:
- `/new`
- `/reset`
- `/stop`
- gateway startup

## Files to create in your workspace

Create a hook folder:

```text
~/.openclaw/workspace/hooks/session-token-ledger/
```

Add these two files there.

### `HOOK.md`

```md
---
name: session-token-ledger
description: "Automatically scans session transcripts and maintains per-session + aggregate token ledgers"
metadata: {"openclaw":{"emoji":"🧾","events":["command:new","command:reset","command:stop","gateway:startup"]}}
---

# Session Token Ledger Hook

Scans OpenClaw session transcript files, sums assistant usage tokens per session, writes one ledger file per session using `YYYY-MM-DD_N.md`, and updates `TOTAL_TOKENS.txt`.

Notes:
- It is idempotent: reruns safely.
- It logs completed transcript content from session files.
- It skips the currently active live `.jsonl` session when a matching `.lock` file exists, so rebuilds default to completed sessions only.
```

### `handler.ts`

```ts
import { spawnSync } from 'node:child_process';
import type { HookHandler } from 'openclaw/hooks';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SCRIPT = path.join(__dirname, 'rebuild_sqlite.py');
const SKILL_DIR = path.join(process.env.HOME || '', '.openclaw', 'workspace', 'skills', 'session-token-ledger');

function rebuildLedger() {
  const result = spawnSync('python3', [SCRIPT, '--skill-dir', SKILL_DIR], { encoding: 'utf8' });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    throw new Error(result.stderr || result.stdout || `rebuild_sqlite.py failed with status ${result.status}`);
  }
}

const handler: HookHandler = async (event) => {
  if (!event || typeof event !== 'object') return;
  const key = `${event.type}:${event.action}`;
  if (!['command:new', 'command:reset', 'command:stop', 'gateway:startup'].includes(key)) return;
  try {
    rebuildLedger();
  } catch (error) {
    console.error('[session-token-ledger] Failed:', error);
  }
};

export default handler;
```

Copy `scripts/rebuild_sqlite.py` from this skill into the same hook folder as `rebuild_sqlite.py`.

The hook passes `--skill-dir` explicitly so the rebuild script writes output into the installed skill directory rather than the hook directory.

## Manual alternative

If you do not want hooks, run this manually whenever the ledger looks stale:

```bash
python3 scripts/rebuild_sqlite.py
```
