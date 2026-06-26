# Review Layers

Walk through each layer in order when reviewing a PR, then produce a verdict.

## 1. Security

- Hardcoded secrets, API keys, tokens in code or config
- SQL/command injection, XSS, SSRF, path traversal
- Missing auth/authz checks on new endpoints
- Sensitive data in logs or error messages
- Public exposure of resources that should be private
- Overly permissive IAM policies or security groups

## 2. Correctness

- Logic errors, off-by-one, null/empty handling
- Error handling gaps (uncaught exceptions, missing fallbacks)
- Race conditions or concurrency issues
- Breaking changes to public APIs or interfaces
- Missing database migrations for schema changes
- Edge cases not covered by the implementation

## 3. Conventions

Check against your team's standards. See [conventions.md](conventions.md) for your team-specific rules.

Common checks (customize or replace):
- Commit message format
- Branch naming conventions
- PR description completeness
- Consistent code style
- Naming conventions (variables, functions, files)

## 4. Infrastructure as Code (when reviewing IaC files)

See [iac-checklist.md](iac-checklist.md) for your team-specific IaC rules.

Common checks:
- Required tags/labels on resources
- Provider version pinning
- State backend configuration
- No hardcoded secrets or account IDs
- Least-privilege IAM policies
- Region/location constraints

## 5. Testing

- New code should have corresponding tests
- Test coverage should not decrease
- Tests are meaningful (not just asserting true)
- CI/CD changes should be validated (dry-run, plan output)
- Edge cases from layer 2 are covered

---

## Verdict Format

After reviewing all layers, produce a structured verdict:

```markdown
## Review: <repo>#<number> — <title>

### Summary
<1-2 sentence assessment. Be direct.>

### 🚨 MUST FIX (<count>)
Issues that block merge.

**[MF-1] <title>**
📍 `<file>:<line>`
Problem: <what's wrong>
Fix: <specific action to take>

### ⚠️ SHOULD FIX (<count>)
Issues worth fixing but not blocking.

**[SF-1] <title>**
📍 `<file>:<line>`
Problem: <what's wrong>
Suggestion: <recommended change>

### 💡 SUGGESTION (<count>)
Optional improvements.

**[SG-1] <title>**
📍 `<file>:<line>`
Suggestion: <improvement>

### ✅ What's Good
<Acknowledge what the PR does well — don't skip this.>

### Verdict
APPROVE / REQUEST CHANGES / COMMENT
<One line justification>
```

## Severity Rules

- **MUST FIX** — merge-blocking. Security vulnerabilities, data loss risk, broken functionality, policy violations.
- **SHOULD FIX** — worth addressing before merge. Convention violations, missing tests, performance issues, inconsistencies.
- **SUGGESTION** — optional. Style preferences, alternative approaches, documentation improvements.

When in doubt, go one severity lower. Don't inflate MUST FIX — it loses meaning if overused.

## Review Commands

```bash
# Fetch PR details and diff
gh pr view <number> --repo <owner/repo> --json title,body,headRefName,baseRefName,files,additions,deletions
gh pr diff <number> --repo <owner/repo>

# Post review
gh pr review <number> --repo <owner/repo> --approve --body "<verdict>"
gh pr review <number> --repo <owner/repo> --request-changes --body "<verdict>"
gh pr review <number> --repo <owner/repo> --comment --body "<verdict>"

# Inline comment on a specific line
gh api repos/<owner/repo>/pulls/<number>/comments \
  -f body="<comment>" \
  -f path="<file>" \
  -F line=<line> \
  -f commit_id="$(gh pr view <number> --repo <owner/repo> --json headRefOid --jq .headRefOid)"
```
