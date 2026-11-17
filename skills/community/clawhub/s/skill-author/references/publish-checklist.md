# Publish Checklist (clawhub CLI)

Exact commands and pre-publish self-check. Everything green before `clawhub publish`.

## Pre-step: diff local vs registry (required before re-releasing)

```bash
# 1. List files on the registry
clawhub inspect <slug> --files

# 2. Pull them to a **fresh, unpredictable** temp folder for comparison
#    (skill-card.md is registry-generated — skip it).
#    Using mktemp -d guarantees a brand-new path every run, so this step can
#    never remove pre-existing files in any predictable location:
STALE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/clawhub-diff.XXXXXX")
trap 'rm -rf "$STALE_DIR"' EXIT
for f in $(clawhub inspect <slug> --files 2>/dev/null | awk 'NR>1{print $1}' | grep -v skill-card.md); do
  mkdir -p "$STALE_DIR/$(dirname $f)"
  clawhub inspect <slug> --file "$f" > "$STALE_DIR/$f" 2>/dev/null
done

# 3. Diff
diff -rq <local skill dir> "$STALE_DIR"
```

Judgment rules:
- Local is a **deliberate superset** (new references, new features) → publish as-is.
- Local is missing files that the registry has (anything besides the auto-generated `skill-card.md`) → add them back first.
- Dead links found (docs reference files that don't exist) → create the file or delete the reference.

## Completeness self-check

| # | Check | Command / method |
|---|-------|-----------------|
| 1 | `SKILL.md` has `name` + `description` (triggers in the first 60 chars) | `head SKILL.md` |
| 2 | Frontmatter has `version` / `license` / `description_zh` / `description_en` / `homepage` / `compatibility` / `allowed-tools` | `head -20 SKILL.md` |
| 3 | Every `references/*.md` cited in docs exists | `grep -oE 'references/[a-zA-Z0-9_-]+\.md' SKILL.md README*.md \| sort -u` then `[ -f ]` each |
| 4 | Every subcommand / env var / file named in docs exists in code | `grep -n "add_parser\|getenv\|environ" <script>` and cross-check |
| 5 | No `__pycache__/`, `test_output/`, `.DS_Store` artifacts | `find . -type d -name __pycache__ -o -name test_output` |
| 6 | No hardcoded private IPs / secrets / personal data | `grep -rnE '\b[0-9]{1,3}(\.[0-9]{1,3}){3}\b|sk_|token|password' --include='*.json' --include='*.md' --include='*.py'` |
| 7 | `LICENSE` exists and matches frontmatter `license` | `ls LICENSE` |
| 8 | `VERSION` exists and equals frontmatter `version` | `cat VERSION` vs frontmatter |
| 9 | Version bumped (semver) and changelog written | — |
| 10 | Logged in | `clawhub whoami` |

## Publish

```bash
cd <parent of the skill folder>
clawhub publish ./<slug> \
  --version X.Y.Z \
  --changelog "<itemized changes — reviewers and installers both read this>"
# success: OK. Published <slug>@X.Y.Z (<versionId>)
```

## Post-publish verification (moderation queue)

After publish, the registry enters a `pending.publication` queue (seconds to a few minutes). Poll:

```bash
for i in 1 2 3 4 5 6; do
  OUT=$(clawhub inspect <slug> 2>&1)
  echo "$OUT" | grep -q "Latest: X.Y.Z" && { echo LIVE; break; }
  echo "$OUT" | grep -E 'Latest:|pending' | head -1
  sleep 25
done
```

- `Latest: X.Y.Z` appears = live.
- Still `pending.publication` after ~10 minutes → check the clawhub.ai page for the review state / any blocker.

## Registry display vs in-package license

The listing page always shows `License: MIT-0` — that is the platform's fixed registration term and does **not** override the in-package `LICENSE` file. Installers get the in-package license; a mismatch is not an error.

## Useful triage commands

```bash
clawhub inspect <slug> --versions --limit 20   # version history
clawhub inspect <slug> --file <path>            # fetch one file raw for comparison
clawhub inspect <slug> --json                   # full metadata
clawhub search "<keywords>"                     # find collisions / related skills
```
