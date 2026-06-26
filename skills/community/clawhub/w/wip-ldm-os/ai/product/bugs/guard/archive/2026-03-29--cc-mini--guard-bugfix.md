# Bug: Branch Guard - Three Bugs in v1.9.56 Destructive Patterns

**Date:** 2026-03-29
**Filed by:** cc-mini
**GitHub Issue:** wipcomputer/wip-ai-devops-toolbox#232
**Related:** #240, #241, wipcomputer/wip-ai-devops-toolbox#231
**Priority:** high

## Context

v1.9.56 added DESTRUCTIVE_PATTERNS to the branch guard. The intent was right (block destructive git commands on all branches), but the implementation introduced three bugs because it was written differently from the existing guard code. The existing guard checks allowed patterns before blocked patterns. The new code skips that step.

Parker's guidance: "Doesn't mean you can't do them; it just means you can't fire them off in rapid succession." The guard is a speed bump, not a wall. But it has to work correctly.

## How the two guards relate (no overlap)

| | File Guard (`wip-file-guard`) | Branch Guard (`wip-branch-guard`) |
|---|---|---|
| **Settings matcher** | `Edit\|Write` | `Write\|Edit\|NotebookEdit\|Bash` |
| **Purpose** | Protect identity/memory files from destructive edits | Protect main branch from all writes |
| **Scope** | Specific files (SOUL.md, MEMORY.md, etc.) | All files in any git repo on main |
| **Watches Bash?** | No | Yes |
| **Branch-aware?** | No (any branch) | Yes (main vs branch vs worktree) |

Both hooks must pass for a tool call to proceed. No overlap. They complement each other.

## Three bugs

### Bug 1: False positive on quoted strings (DESTRUCTIVE_PATTERNS)

**Repro:** `gh issue create --body "use git checkout -- to fix"`
**Expected:** ALLOW (gh is a safe command, quoted text is data)
**Actual:** BLOCKED (regex matches `git checkout --` inside the body text)
**Root cause:** DESTRUCTIVE_PATTERNS (line 245) fires before any allowed check. Raw regex against entire command string.

### Bug 2: False negative on compound commands (ALLOWED fast-path)

**Repro:** `cd /repo && rm -f file ; echo done`
**Expected:** DENY on main (rm is blocked)
**Actual:** ALLOW (the allowed fast-path at line 418 matches `/\becho\b/` and exits)
**Root cause:** The allowed check tests the entire command string. `echo` on a different command segment excuses `rm -f`.

### Bug 3: False positive on quoted strings (BLOCKED patterns on main)

**Repro:** `echo "don't run git commit on main"`
**Expected:** ALLOW (echo is safe, quoted text is data)
**Actual:** BLOCKED (`/\bgit\s+commit\b/` matches inside the quoted string)
**Root cause:** Same as Bug 1. The blocked patterns at lines 425-452 also match against the raw command string.

## The fix

Two helper functions. Four edit sites. No architectural changes.

### Helper 1: `stripQuotedContent(cmd)`

```javascript
function stripQuotedContent(cmd) {
  return cmd.replace(/"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/g, '""');
}
```

Replaces quoted string contents with `""` before regex matching. Handles escaped quotes.

### Helper 2: `isBlockedCompoundCommand(cmd, blocked, allowed)`

```javascript
function isBlockedCompoundCommand(cmd, blockedPatterns, allowedPatterns) {
  const stripped = stripQuotedContent(cmd);
  const segments = stripped.split(/\s*(?:&&|\|\||[;|])\s*/).filter(Boolean);
  for (const segment of segments) {
    if (blockedPatterns.some(p => p.test(segment))) {
      if (!allowedPatterns.some(p => p.test(segment))) return true;
    }
  }
  return false;
}
```

Splits compound commands on `&&`, `||`, `;`, `|`. Checks each segment independently. An allowed pattern on one segment can't excuse a blocked pattern on a different segment.

### Split DESTRUCTIVE_PATTERNS

```javascript
// Git commands: checked against STRIPPED command (no quoted content)
const DESTRUCTIVE_PATTERNS = [
  /\bgit\s+clean\s+-[a-zA-Z]*f/,
  /\bgit\s+checkout\s+--\s/,
  /\bgit\s+checkout\s+\.\s*$/,
  /\bgit\s+stash\s+drop\b/,
  /\bgit\s+stash\s+pop\b/,
  /\bgit\s+stash\s+clear\b/,
  /\bgit\s+reset\s+--hard\b/,
  /\bgit\s+restore\s+(?!--staged)/,
];

// Code execution bypasses: checked against ORIGINAL command
// (because python -c "open()" IS the attack, it's supposed to be inside quotes)
const DESTRUCTIVE_CODE_PATTERNS = [
  /\bpython3?\s+-c\s+.*\bopen\s*\(/,
  /\bnode\s+-e\s+.*\bfs\.\w*[Ww]rite/,
];
```

### Four edit sites

1. **Flow A (lines 243-262):** Use `strippedCmd` for DESTRUCTIVE_PATTERNS, original cmd for DESTRUCTIVE_CODE_PATTERNS
2. **"Not in worktree" check (line 378):** Replace inline check with `isBlockedCompoundCommand`
3. **Remove fast-path (lines 417-420):** Delete the early-exit allowed check. This is Bug 2.
4. **Flow B blocked checks (lines 425-452):** Replace both loops with `isBlockedCompoundCommand`

### Also: add plan files to SHARED_STATE_PATTERNS

The guard blocks editing `~/.claude/plans/*.md` because `~/.claude/` is a git repo on main. Plan files should be editable. Add:

```javascript
/\.claude\/plans\//,
```

## Test cases

| Command | Branch | Expected | Bug |
|---------|--------|----------|-----|
| `gh issue create --body "git checkout -- file"` | any | ALLOW | 1 |
| `rm -f file ; echo done` | main | DENY | 2 |
| `echo "don't run git commit"` | main | ALLOW | 3 |
| `python3 -c "open('f').write('x')"` | any | DENY | still works |
| `git checkout main` | main | ALLOW | no regression |
| `git worktree add .worktrees/x -b feat` | main | ALLOW | no regression |
| `git checkout -- file.txt` | any | DENY | no regression |
| `git stash list` | main | ALLOW | no regression |
| `ls -la && echo done` | main | ALLOW | no regression |

## Files to change

| File | What |
|------|------|
| `tools/wip-branch-guard/guard.mjs` | Add 2 helpers, split destructive arrays, fix 4 edit sites, add plan files to shared state |
| `tools/wip-branch-guard/package.json` | Version bump to 1.9.59 |

## 5 Questions

1. **Source files:** guard.mjs, package.json in wip-branch-guard
2. **ldm install deploys:** Updated guard to ~/.ldm/extensions/wip-branch-guard/
3. **Fresh vs existing:** Same behavior but fewer false positives/negatives
4. **Docs:** None (internal bugfix)
5. **Files touched:** ~/.ldm/extensions/wip-branch-guard/guard.mjs
