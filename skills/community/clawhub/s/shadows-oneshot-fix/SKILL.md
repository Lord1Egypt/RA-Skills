---
name: oneshot-fix
description: "Surgical quick fix — max 5 tool calls, zero exploration, read-diagnose-fix-verify. Use for small bugs, typos, simple changes that don't need deep analysis."
metadata: { "openclaw": { "emoji": "⚡", "homepage": "https://clawhub.ai/NakedoShadow", "os": ["darwin", "linux", "win32"] } }
---

# Oneshot Fix — Surgical Quick Fix

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Small, clearly-defined bug with known location
- Simple typo or naming fix
- User says "quick fix", "oneshot", "just fix it"
- Single-file change with obvious solution
- Configuration tweak or value change

## WHEN NOT TO TRIGGER

- Root cause is unknown (use bug-hunter instead)
- Multiple files need coordinated changes
- Architectural decision required (use deep-research)
- User wants exploration or brainstorming

---

## PREREQUISITES

No specific binaries required. The verification step (Phase 4) auto-detects available tools:

- `python` — Used for `python -m py_compile {file}` syntax check on `.py` files. Detected via `which python` or `which python3`.
- `npx` — Used for `npx tsc --noEmit {file}` type check on `.ts` files. Detected via `which npx`.
- `pytest` / `jest` / `vitest` — Used for running a targeted test if a test file is specified. Detected via standard tool resolution.

If no compiler or test runner is available for the target file type, the verification step is skipped gracefully and the agent reports that manual verification is recommended.

---

## CONSTRAINTS

- **Maximum 5 tool calls** total (read + fix + verify)
- **Zero exploration** — go directly to the target
- **No brainstorming** — the path is clear, just execute
- **No new files** — edit existing code only
- **Minimal diff** — change only what's necessary

---

## PROTOCOL

### Step 1 — READ (1 tool call)

Read the target file. If user specified a line number, use offset/limit to read only the relevant section.

### Step 2 — DIAGNOSE (0 tool calls — mental only)

In your head:
- What's wrong?
- What's the minimal fix?
- Will this break anything else?

### Step 3 — FIX (1-2 tool calls)

Apply the fix using Edit tool. Change ONLY the broken part.

Rules for the fix:
- Same coding style as surrounding code
- No additional refactoring
- No "while I'm here" improvements
- No new comments or docstrings unless they were the bug

### Step 4 — VERIFY (1 tool call)

Run the appropriate check based on file type:
```bash
# Python — syntax check
python -m py_compile {file}

# TypeScript — type check (suppress non-critical output)
npx tsc --noEmit {file} 2>/dev/null

# Run specific test if applicable
python -m pytest {test_file} -x -q 2>/dev/null
```

If no verification tool is available, report: "No compiler/test runner detected for this file type. Manual verification recommended."

---

## RULES

1. **5 tool calls MAX** — if you need more, switch to bug-hunter skill
2. **Smallest possible diff** — touch nothing extra
3. **Match existing style** — no reformatting, no "improvements"
4. **Verify always** — even quick fixes need a sanity check
5. **If unsure, escalate** — don't guess on a oneshot, use a proper debug skill

---

## SECURITY CONSIDERATIONS

- **Commands executed**: Optional compile check (`python -m py_compile`, `npx tsc --noEmit`) or test run (`pytest`, `jest`, `vitest`) in the verification step. These execute local code in the repository.
- **Data read**: Source files in the local repository (1-2 files maximum).
- **File modification**: Edits the target source file with a minimal diff.
- **Network access**: None.
- **Persistence**: None.
- **Credentials**: None required.
- **Sandboxing**: The verification step runs local code (compile/test). Safe for trusted repositories. For untrusted code, skip verification or run in a sandbox.

---

## OUTPUT FORMAT

```
Fixed: [one-line description]
File: [path:line]
Change: [old] -> [new]
Verified: [compilation/test result]
```

That's it. No report, no analysis, no recommendations. Just the fix.

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
