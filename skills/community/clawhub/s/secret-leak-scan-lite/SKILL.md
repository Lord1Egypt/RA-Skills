---
name: secret-leak-scan-lite
description: Statically scan a project directory for leaked credentials (AWS access keys, GitHub PATs, Slack tokens, private-key blocks) before committing. Prints a JSON report with masked fingerprints only — raw secret values are never emitted. Use when the user asks to check a folder for leaked secrets, exposed keys, or committed credentials.
---

# Secret Leak Scan (Lite)

Scan files **the user owns or is authorized to analyze** for accidentally committed credentials, using the bundled `scripts/scan.mjs`, and turn the JSON report into a remediation list.

## Scope and rules

- Only scan paths the user supplied or confirms they are authorized to inspect. If authorization is unclear, ask before running anything.
- The scanner is static: it reads files and matches patterns. It never executes the scanned code and never follows symlinks.
- Never try to recover, print, or reuse a detected secret. Report findings only by the type, file, line, and masked fingerprint the tool provides, and recommend rotation.
- Do not overclaim. Zero findings means none of the known patterns matched — it does not prove the tree is secret-free.

## 1. Run

Requires Node 18 or later. The script is bundled with this skill:

```bash
node <skill-dir>/scripts/scan.mjs <directory>
```

- Stdout is the JSON report (safe to pipe to a file); diagnostics go to stderr.
- Exit codes: `0` no findings, `1` findings present, `2` usage/read error.

## 2. Read the JSON report

- `summary`: `filesScanned`, `filesSkipped` (over 5 MB or unreadable), `findings` count, and `byType` breakdown.
- `findings[]`: `type` (`aws-access-key-id`, `github-personal-access-token`, `slack-token`, `private-key-block`), `file`, `line`, `fingerprint` (`ABCD… (len=N, sha256:xxxxxxxx)`).
- `notes`: skipped files and suppressed matches (per-file cap of 20).

## 3. Triage

Treat **every** finding as a potentially live credential. For each one:

1. Open `file:line` and confirm the match is a real credential, not a documented example (e.g. AWS's `REDACTED-SECRET`).
2. Recommend rotation, not just deletion: revoke the key or token at the provider. Assume anything committed is compromised — it also stays in git history until purged.
3. Prevent recurrence: move the value to environment variables or a secrets manager, and add the file to `.gitignore`.

## 4. Deliver

```
Secret scan: <input path>   (<filesScanned> files, <filesSkipped> skipped)

Findings (<n>)
- <type> — <file>:<line> — fp: <fingerprint> — action: <rotate at X>

Notes
- <skipped/unreadable items, or "none">
```

Rules for the review:
- Quote the fingerprint so the user can correlate findings without exposing values.
- Never state the tree is "clean" or "secure"; say which patterns were checked.

## Full version

This is the lite edition — directory scans and the four most common credential types. The full `secret-leak-scan` skill adds `.asar` bundle scanning, Stripe/Google/fine-grained-PAT patterns, a complete triage-and-rotation workflow, git-history cleanup steps, and a CI gate recipe.
