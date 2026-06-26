# Plan: Repo Review — Code Quality & Infrastructure Improvements

**Status:** Upcoming
**Filed:** 2026-03-19
**Tickets:** See `2026-03-19--repo-review-issues.json` for GitHub issue payloads

## Context

Full repository review of wip-ldm-os identified 9 improvements across code quality, testing, CI/CD, and developer experience. The architecture and safety patterns are strong — these issues address gaps that will matter as the project scales and gains contributors.

## Phase 1: Critical Fix (Do First)

### 1a. Remove hardcoded user path in bridge (#P1)

**File:** `src/bridge/core.ts` line 13
**Problem:** `const HOME = process.env.HOME || "/Users/lesa"` leaks a developer path and breaks for other users.
**Fix:** Replace with `os.homedir()`:
```typescript
import { homedir } from 'node:os';
const HOME = process.env.HOME || homedir();
```

**Effort:** 5 minutes

## Phase 2: Testing & CI (High Priority)

### 2a. Add test infrastructure (#P2)

Set up a minimal test framework. Recommended: Node's built-in `node:test` runner (zero deps, aligns with the project's philosophy).

**New files:**
- `test/lib/deploy.test.mjs` — deployment engine unit tests
- `test/lib/state.test.mjs` — state reconciliation tests
- `test/lib/safe.test.mjs` — safe file operations tests
- `test/bridge/core.test.ts` — config resolution tests

**package.json changes:**
```json
"scripts": {
  "test": "node --test test/**/*.test.mjs",
  "test:bridge": "npx tsx --test test/bridge/*.test.ts"
}
```

**Priority test targets (by risk):**
1. `lib/safe.mjs` — trash-instead-of-delete is a safety net; test it first
2. `lib/deploy.mjs` — 1000+ lines of critical deployment logic
3. `lib/state.mjs` — state reconciliation bugs could cause data loss
4. `src/bridge/core.ts` — config resolution, API key lookup

**Effort:** 2-4 hours for initial coverage

### 2b. Add GitHub Actions CI (#P3)

**New file:** `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build:bridge
      - run: npm test
```

**Effort:** 30 minutes

## Phase 3: Code Quality (Medium Priority)

### 3a. Break up bin/ldm.js into command modules (#P4)

**Problem:** `bin/ldm.js` is 2,600+ lines handling 9+ commands. Hard to navigate, review, or test.

**Proposed structure:**
```
bin/
  ldm.js              (slim dispatcher — parse args, route to command)
  commands/
    init.mjs
    install.mjs
    doctor.mjs
    status.mjs
    sessions.mjs
    msg.mjs
    updates.mjs
    worktree.mjs
```

Each command module exports a single `run(args, opts)` function. Shared helpers (console formatting, lockfile, registry access) move to `lib/cli-helpers.mjs`.

**Effort:** 3-5 hours (incremental — can do one command at a time)

### 3b. Replace silent catch blocks with logging (#P5)

**Problem:** Multiple `catch {}` blocks suppress errors entirely:
- `lib/deploy.mjs:203`
- `lib/state.mjs:79`
- `bin/ldm.js:150-152`
- Several more across the codebase

**Fix:** Add a lightweight debug logger:
```javascript
// lib/log.mjs
const DEBUG = process.env.LDM_DEBUG === '1';
export function debug(context, msg, err) {
  if (DEBUG) console.error(`[ldm:${context}] ${msg}`, err?.message || '');
}
```

Replace `catch {}` with `catch (err) { debug('deploy', 'optional step failed', err); }`.

Users can opt-in with `LDM_DEBUG=1 ldm install`.

**Effort:** 1-2 hours

### 3c. Add linting and formatting (#P6)

**Problem:** No ESLint or Prettier config. Style drift is likely with multiple contributors (including AI agents).

**Recommendation:** Minimal Prettier config only (avoid heavy ESLint rules for a zero-deps project):

```json
// .prettierrc
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100
}
```

```json
// package.json scripts
"fmt": "npx prettier --write 'src/**/*.{ts,mjs}' 'lib/**/*.mjs' 'bin/**/*.js'",
"fmt:check": "npx prettier --check 'src/**/*.{ts,mjs}' 'lib/**/*.mjs' 'bin/**/*.js'"
```

Add `fmt:check` to CI pipeline.

**Effort:** 1 hour (config + initial format pass)

## Phase 4: Small Improvements (Low Priority)

### 4a. Use fs.rmSync instead of shell rm -rf (#P7)

**File:** `lib/deploy.mjs` line ~709
**Problem:** `execSync('rm -rf ...')` has a shell injection surface and isn't cross-platform.
**Fix:** Replace with `fs.rmSync(path, { recursive: true, force: true })`.

**Effort:** 15 minutes

### 4b. Add engines field to package.json (#P8)

**Problem:** SKILL.md says Node 18+ required but package.json doesn't enforce it.
**Fix:**
```json
"engines": {
  "node": ">=18"
}
```

**Effort:** 5 minutes

### 4c. Stop committing dist/ to git (#P9)

**Problem:** `dist/bridge/` is compiled output checked into git.
**Fix:**
1. Add `dist/` to `.gitignore`
2. Add `"prepublishOnly": "npm run build:bridge"` to package.json scripts
3. Remove `dist/` from git tracking: `git rm -r --cached dist/`

**Note:** Only do this if npm publish workflow can run a build step. If publishing from CI, this is straightforward. If publishing manually, the prepublishOnly hook handles it.

**Effort:** 15 minutes

## Execution Order

```
Phase 1 (now)     → Hardcoded path fix (5 min, ship immediately)
Phase 2a (next)   → Tests for lib/safe.mjs, then expand
Phase 2b (next)   → CI pipeline (can parallel with 2a)
Phase 3a (later)  → Break up ldm.js (incremental, one command per PR)
Phase 3b (later)  → Debug logging (can do alongside 3a)
Phase 3c (later)  → Prettier (one-time format commit, then enforce in CI)
Phase 4 (anytime) → Small fixes, can be bundled into any PR
```

## Out of Scope

- Feature work (new commands, new protocols)
- Refactoring bridge TypeScript (already clean)
- Documentation updates (already thorough)
- Performance optimization (not a current bottleneck)
