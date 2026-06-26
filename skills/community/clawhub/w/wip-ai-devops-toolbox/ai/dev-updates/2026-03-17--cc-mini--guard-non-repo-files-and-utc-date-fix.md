# Guard non-repo files fix + UTC date fix

Two bugs fixed in one PR.

## Bug 1: Guard blocks files outside git repos (#77)

**Problem:** When Write/Edit targets a file outside any git repo (e.g. `~/.claude/plans/`), `findRepoRoot()` returns null. The guard fell back to CWD (`~/.openclaw` on main) and blocked the operation. Files outside repos aren't the guard's concern.

**Fix:** If `findRepoRoot(filePath)` returns null for Write/Edit operations, allow immediately. The guard only protects git repos from direct-on-main edits.

**File:** `tools/wip-branch-guard/guard.mjs`

## Bug 2: UTC date mismatch in wip-release

**Problem:** Dev-update files are named with local date (e.g. `2026-03-16--cc-mini--...md`). But `new Date().toISOString().split('T')[0]` returns UTC date. After midnight UTC (4 PM PST), the dates diverge. Release notes gate fails to find today's dev-update.

**Fix:** Replaced all three instances of `toISOString()` date extraction with explicit local date construction using `getFullYear()/getMonth()/getDate()`.

**Files:**
- `tools/wip-release/cli.js` (line 80, dev-update detection)
- `tools/wip-release/core.mjs` (line 92, CHANGELOG date)
- `tools/wip-release/core.mjs` (line 582, product docs sync date)
