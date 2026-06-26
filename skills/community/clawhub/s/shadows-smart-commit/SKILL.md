---
name: smart-commit
description: "Intelligent git commit assistant — analyzes diffs, enforces conventional commits, detects secrets, generates meaningful messages. Use when committing code changes."
metadata: { "openclaw": { "emoji": "🔒", "homepage": "https://clawhub.ai/NakedoShadow", "requires": { "bins": ["git"] }, "os": ["darwin", "linux", "win32"] } }
---

# Smart Commit — Intelligent Git Commit Assistant

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- User says "commit", "smart commit", "save my changes", or "push"
- After completing a coding task when changes need to be committed
- User asks to review and commit staged changes

## WHEN NOT TO TRIGGER

- User explicitly says "don't commit" or "no commit"
- No changes exist in the working tree (`git status` shows clean)
- User is just browsing or reading code

---

## PREREQUISITES

This skill requires only `git` on PATH. All commands are standard git operations that read repository state and create commits. No network access, no external APIs, no additional toolchains required.

---

## PROCESS

### Phase 1 — Reconnaissance

Run these commands to understand the current state:

```bash
git status
git diff --cached --stat
git diff --stat
git log --oneline -5
```

Analyze:
1. What files changed (staged vs unstaged)
2. The nature of changes (new feature, bugfix, refactor, docs, test, chore)
3. Recent commit style to match existing conventions

### Phase 2 — Security Scan (MANDATORY)

Before ANY commit, scan staged changes for leaked secrets:

```bash
# Scan staged diff for secret patterns
git diff --cached | grep -inE "(api[_-]?key|secret|token|password|credential|private[_-]?key)\s*[:=]\s*['\"][^'\"]{8,}" || echo "PASS: No secrets detected in staged changes"
```

**If secrets detected**: STOP immediately. Warn the user with the exact file:line. Do NOT proceed with the commit.

Check for files that should never be committed:
```bash
# Check if dangerous files are staged
git diff --cached --name-only | grep -iE "\.(env|pem|key|p12|pfx)$|credentials|secret" || echo "PASS: No sensitive files staged"
```

Blocked file patterns: `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `*credentials*`, `*secret*`, `node_modules/`, `__pycache__/`, `.DS_Store`

**Limitations**: This grep-based scan catches common patterns but may produce false positives (e.g., test fixtures with "password" in variable names) or miss obfuscated secrets. For high-security projects, complement with gitleaks or trufflehog.

### Phase 3 — Staging Strategy

- **NEVER** use `git add .` or `git add -A` — these can accidentally include sensitive files
- Stage files individually by name: `git add src/feature.ts tests/feature.test.ts`
- Group related files logically in the same commit
- If unrelated changes exist, suggest splitting into multiple atomic commits

### Phase 4 — Commit Message Generation

Follow **Conventional Commits** specification (conventionalcommits.org):

```
type(scope): concise description

[optional body explaining WHY, not WHAT]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `style`, `build`, `ci`

**Rules**:
- Subject line: max 72 characters, imperative mood ("add" not "added")
- Focus on WHY, not WHAT (the diff shows WHAT)
- Include scope when changes are localized to a module
- Use HEREDOC for multi-line messages to preserve formatting:
  ```bash
  git commit -m "$(cat <<'EOF'
  type(scope): subject line

  Body explaining the motivation.

  Co-Authored-By: Claude <noreply@anthropic.com>
  EOF
  )"
  ```

### Phase 5 — Verification

After commit, verify success:
```bash
git log --oneline -1
git status
```

Confirm: commit SHA visible, working tree status as expected.

---

## SECURITY CONSIDERATIONS

1. **Read-only analysis**: Phases 1-2 only read git state (status, diff, log). No files are modified, no network calls are made.

2. **Secret detection output**: Phase 2 may display matched secret-like patterns in terminal output. Run in a secure terminal where output is not forwarded to shared logging systems.

3. **Write operations**: Phase 3 (`git add`) and Phase 4 (`git commit`) modify git state. These are local operations — no data is pushed to any remote unless the user explicitly requests `git push` afterward.

4. **No persistence**: This skill does not store credentials, modify config files, or install packages. Each invocation is stateless.

5. **No network access**: The entire workflow is local. `git push` is never executed unless the user explicitly requests it as a separate step.

---

## OUTPUT FORMAT

```markdown
## Changes Detected
- [file list with change type: added/modified/deleted]

## Security Scan
- Secrets in diff: [PASS — none detected / FAIL — found at file:line]
- Sensitive files: [PASS — none staged / FAIL — list of files]

## Proposed Commit
type(scope): message

## Files to Stage
- [explicit file list, one per line]

## Post-Commit
- SHA: [short hash]
- Status: [clean / remaining unstaged changes]
```

---

## RULES (by priority)

1. **Security first** — NEVER commit secrets, tokens, API keys
2. **Specific staging** — NEVER `git add .` — always name files explicitly
3. **Conventional format** — `type(scope): message` always
4. **Meaningful messages** — explain intent, not just what changed
5. **No force push** — NEVER `git push --force` on main/master
6. **No amend** — create NEW commits unless explicitly asked to amend
7. **No skip hooks** — NEVER use `--no-verify`
8. **Atomic commits** — one logical change per commit

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
