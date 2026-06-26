# Skill Lint

Validate and fix SKILL.md frontmatter issues automatically.

## Scan Paths

1. `~/.claude/skills/` - Personal skills
2. `~/.claude/plugins/marketplaces/*/plugins/*/skills/` - Plugin skills
3. `.claude/skills/` - Project skills

## Validation Rules

### Common Fields (Ordered)

| Field | Required | Description |
|-------|----------|-------------|
| `name:` | **Yes** | Skill name (must match directory) |
| `description:` | **Yes** | Description + trigger keywords. **Length ≤ 1024 chars** (see below) |

### Description Length Budget (HARD STOP)

**`description` field must be ≤ 1024 characters.** Claude Code's system reminder truncates descriptions beyond the limit, dropping trigger keywords at the tail — which causes skill discovery failures.

**Measure** (3-layer fallback — first available wins):

```bash
# Layer 1 (preferred — uses upstream YAML parser, exits cleanly on all frontmatter shapes)
DESC=$(skills-ref read-properties <skill-dir> 2>/dev/null | jq -r '.description // ""')

# Layer 2 (when skills-ref unavailable but Python+PyYAML present)
DESC=$(python3 -c "
import yaml
parts = open('SKILL.md').read().split('---', 2)
print(yaml.safe_load(parts[1]).get('description','') or '', end='')
")

# Layer 3 (awk fallback — block-scalar aware, exits on next top-level key or end of frontmatter)
DESC=$(awk '
  BEGIN { fm=0; in_desc=0 }
  /^---$/ { fm++; if (fm==2) exit; if (in_desc) exit; next }
  fm==1 {
    if (in_desc) {
      if (/^[A-Za-z_][A-Za-z0-9_-]*:/) exit          # next top-level key terminates block scalar
      sub(/^  /, ""); printf "%s", $0; next
    }
    if (/^description:[[:space:]]*\|/)  { in_desc=1; next }
    if (/^description:[[:space:]]/)     { sub(/^description:[[:space:]]*/,""); printf "%s", $0; exit }
  }
' SKILL.md)

echo "len: ${#DESC}"
# Expected: ≤ 1024. If over → truncate or split topics.
```

**Why 3-layer (HARD STOP — historical bug)**: A naive `awk '/^description:/,/^---$/' SKILL.md | sed -E 's/^description: //; /^---$/d'` works **only when `description:` is the LAST key in the frontmatter**. If any other key (`depends-on`, `triggers`, `metadata`, `allowed-tools`) follows `description:`, that key's value is also captured and the measured length is inflated. The 3-layer fallback above (a) uses `skills-ref` which delegates to the upstream YAML parser (most accurate), (b) Python `yaml.safe_load` (parser-correct), (c) an awk that terminates at the next top-level key (boundary-aware). Pick the first layer whose dependency is available — do not fall back to the naive range pattern.

**Reduction strategies (in priority order)**:

| # | Strategy | Example |
|---|----------|---------|
| 1 | Compress `Use when` keyword list | Remove redundant synonyms (e.g., "session ID", "current session", "session id" → keep one) |
| 2 | Shorten topic descriptions to ≤ 40 chars each | `list - enumerate current-project sessions (UUID + mtime + size)` → `list - enumerate sessions` |
| 3 | Drop locale-duplicate keywords | If English and Korean keywords overlap meaning, keep one per concept |
| 4 | Move detail to topic .md files | Topic .md files are unbounded — push verbose explanations there, keep description terse |

**Don't / Do table (HARD STOP — derived from 5 cumulative violators 2026-05-23)**:

| # | Don't (overweight pattern) | Do (canonical compression) | Real violation case |
|---|---------------------------|---------------------------|---------------------|
| 1 | Append new topic description without measuring current length | `wc -c` or awk-length check before Edit; if `current + new > 1024`, compress first | claude-session: 1480 → 1547 over limit |
| 2 | Locale-mix in description (English skill with non-English keywords, or vice versa) | Single locale only. **English skill = 0 non-English keywords** (no "core noun" exception). Non-English skill = native keywords primary, English allowed only for proper nouns/technical terms (Vault, ArgoCD, K3s, etc.). See `opensource.md` "Skill language = description language" HARD STOP | ralph: an English keyword paired with two transliterated synonyms (`"ralph update"+"ralph <update-localized>"+"ralph <latest-localized>"`) → If ralph is an English skill, keep only the English form. If localized, keep only one localized form. No mix. |
| 3 | Multiple English synonym variants for the same action | One canonical verb + one canonical noun. No `"X fix"+"fix X"+"update X"+"modify X"` chains | skill-kit: `"skill upgrade"+"skill fix"+"fix skill"+"update skill"` → `"skill upgrade"` only |
| 4 | Topic description over 40 chars or with Step numbers / parenthetical context | Topic description = `<topic> - <one-liner ≤ 40 chars>`. Move Step numbers / nested context to topic .md | consolidate: `internal - Step 3.5 Internal Code Review fallback (CodeRabbit Free walkthrough only / Copilot failure) + Step 4.5 UI capture verification` → `internal - CodeRabbit fallback review` |
| 5 | Append `[filename.md]` to topic descriptions | Topics table already has the file path. description has topic + one-liner only | github-flow: 8x `[xxx.md]` removed (~100 chars saved) |
| 6 | Verbose prose context inside description (full sentences, "Applies to..." paragraphs) | description = one-line skill purpose + topic enumeration + Use when. Prose belongs in topic .md or SKILL.md body | code-workflow: `Applies to all tasks requiring code changes... TDD (Red→Green→Refactor) is applied by default... For GitHub repos, github-flow is the default companion...` → removed (~300 chars saved) |
| 7 | Localized keyword conjugation variants (multiple inflections of the same concept, e.g. "tidy"+"sync"+"items" all referring to the same fix_plan operation) | One canonical conjugation per concept (usually `noun + verb-stem` or a single verb) | ralph: 5 conjugated variants of "fix_plan tidy/sync/items/done-move/Completed-move" → keep only `"fix_plan tidy"` (one canonical form). The unused variants were inflectional duplicates of the same intent |
| 8 | Mix other frontmatter fields (`allowed-tools:`, `depends-on:`) into description text | Each YAML field on its own line. description ends before next field | consolidate: `triggers.allowed-tools: [Agent...]depends-on: [superpowers]` mixed into description tail — separate to own fields |
| 9 | Trust system reminder display ("looks fine to me") | System reminder truncates with `…`. Always measure with `wc` or awk every Edit | claude-session: `"sess…"` truncate confirmed in system reminder |

**Self-check (every time before Edit on `description:` field)**:
1. Measure current length (3-layer fallback — `skills-ref read-properties` → `python yaml.safe_load` → boundary-aware awk; **never** use the legacy `/^description:/,/^---$/` range pattern alone — it over-counts when `description:` is not the last frontmatter key)
2. Estimate new length after Edit
3. If `> 1024`, apply reduction strategies #1~4 + Don't/Do patterns #1~9 first
4. Re-measure after Edit. Confirm ≤ 1024
5. Verify Topics table is the authoritative source for `[filename.md]` references — description should NOT repeat them

**Violation cases (cumulative — system-wide non-compliance)**:
- 2026-05-23 (1st flagged): `claude-session` 1547 chars after `list` topic added → user pointed it out
- Pre-existing violations (cumulative): `github-flow` 2116, `ralph` 1506, `code-workflow` 1269, `consolidate` 1187, `skill-kit` 1091 — all over 1024. Strengthen this rule + run `/skill-kit lint --fix` across skills to bring under limit

### `description:` value must use `|` block scalar when it contains a colon (HARD STOP)

The strict YAML parser used downstream (e.g. `skills-ref validate`) treats an unquoted `:` followed by whitespace as the start of a new mapping. When this appears inside the `description:` value — most commonly via phrases like `Use when: "..."`, `workflow: inventory, ...`, or any localized variant such as a topic-list prefix followed by `:` — the parser raises:

```
invalid YAML: mapping values are not allowed in this context at line N column M
```

The skill is then silently skipped from registration ("Skipped loading N skill(s) due to invalid SKILL.md files"), even though Claude Code's lenient parser would have accepted the same file.

**The rule**: whenever `description:` contains a `:` followed by whitespace (i.e. anything that *looks* like a YAML mapping start), wrap the value in a `|` block scalar so the parser treats every following line as multi-line literal text.

#### Don't / Do

> **Notation note**: `\|` in the table cells below is **markdown table-cell escaping** for the literal YAML pipe character. In actual YAML frontmatter, type the unescaped `|` (see the Canonical form snippet below for a copy-pasteable example).

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|--------------------------|
| 1 | `description: ... Use when: "keyword 1", "keyword 2" ...` (inline scalar with unquoted `:`) | `description: \|` on its own line, then the description body indented two spaces. The body may keep its `:` characters verbatim |
| 2 | "Claude Code parses it fine, so it must be valid YAML" | Claude Code's parser is lenient; strict parsers like `strictyaml` (used by `skills-ref validate`) are stricter. Validate against the strict parser, not the lenient one |
| 3 | Quote the whole value with `"..."` to dodge the parser error | Escaping nested quotes inside an already quote-heavy description (`"Use when: \"keyword\""`) is fragile. The `\|` block scalar form has no escaping requirement |
| 4 | Strip the `:` (rewrite `Use when:` as `Use when`) to silence the parser | Information loss. Use `\|` block scalar instead and keep the colon |
| 5 | Apply `\|` only when the lint already failed | Apply preemptively whenever the description contains `: ` (colon-space). Avoids the "fail → fix → re-validate" cycle |

#### Canonical form

```yaml
---
name: <skill>
description: |
  One-line skill purpose. Topics — a (foo), b (bar). Use when: "trigger 1", "trigger 2" triggers.
metadata:
  author: <author>
  version: "0.1.0"
---
```

The `|` literal block scalar starts on the same line as `description:`; the body lives on the following indented lines (2 spaces is conventional). `metadata:` follows the description block scalar at the same top-level indent — `description: |` plus its indented body ends cleanly when the next non-indented key (`metadata:`) starts. `metadata:` is included here because the host loader's allowlist accepts it and 20/20 published skills use it — omitting it from the canonical example causes new skills to be written without it.

#### Self-check (every time before Edit on `description:` field)

1. Does the new `description:` value contain `: ` (colon followed by whitespace) anywhere in the body? — grep for `: ` inside the staged value
2. If yes, is the value already on a `|` block scalar? — verify the line containing `description:` ends with `|` and the body is indented
3. If not, convert to `|` block scalar before saving
4. After saving, run `skills-ref validate <SKILL.md>` (or equivalent strict-YAML check) — confirm the file parses

#### Violation cases (2026-06-04)

Three skills failed `skills-ref validate` simultaneously, with **two distinct strictyaml error families** at play. The lint rule above addresses the **colon-in-scalar** family. `git-repo` also exhibited a separate **flow-mapping** family — listed below for completeness so a future diagnosis does not collapse the two into one cause.

| Skill | strictyaml error column | Error family | Offending text |
|-------|-------------------------|--------------|----------------|
| `ralph` | line 3, col 687 | colon-in-scalar | `description:` body contained `Use when: "ralph update", ...` |
| `git-repo` (cause A) | line 6, col 810 | colon-in-scalar | `description:` body contained `worktree - unified worktree acquisition workflow: inventory, reuse inactive, or create new ...` |
| `git-repo` (cause B) | line 4 (frontmatter) | flow-mapping (separate family) | `depends-on: [commit-tidy]` — strictyaml rejects JSON-flavored flow mappings in frontmatter. Fixed by converting to block-style list (`depends-on:` then `  - commit-tidy` on the next indented line) |
| `rule-kit` | line 2, col 170 | colon-in-scalar | `description:` body contained a Korean topic-list label (a single Korean word) immediately followed by `: a (...), b (...), c (...), d (...)` — same `<label>: <comma-list>` parser shape as the cases above, just with a non-ASCII label |

The colon-in-scalar family was fixed by converting `description:` to `description: \|` and leaving the body's colons untouched. The flow-mapping family is orthogonal and is fixed by converting `[...]` and `{...}` shorthands to block style. The lint rule above codifies the colon-in-scalar family so the same break does not have to be diagnosed three more times for three more skills; the flow-mapping family is a separate scope-expansion candidate.

### Invalid Fields

| Invalid | Correct | Action |
|---------|---------|--------|
| `tools:` | `allowed-tools:` | Rename field |
| `trigger:` | (remove) | Move keywords to description |
| `triggers:` | (remove) | Move keywords to description |
| `<example>` in description | (remove) | `<example>` is agent-only syntax. Remove from skills. |

### Frontmatter Field Order (Canonical Order)

Frontmatter fields follow this order for readability. lint --fix will reorder automatically.

```yaml
---
name:                      # 1. Required (skill identifier)
description:               # 2. Required (block scalar `|` when body contains `:`)
metadata:                  # 3. Author/version metadata (20/20 published skills use it)
depends-on:                # 4. Dependencies
triggers:                  # 5. Hook triggers
allowed-tools:             # 6. Optional
agent:                     # 7. Optional
context:                   # 8. Optional
hooks:                     # 9. Optional
model:                     # 10. Optional
user-invocable:            # 11. Optional
---
```

**Rationale**: required fields (`name`, `description`) come first because every skill has them and they are scanned first by the loader; `metadata` follows because it is structural-but-optional (almost universally used). Hook-mechanism fields (`depends-on`, `triggers`) follow; tool/agent/runtime config trails.

**Order validation rules:**
- Required fields (`name`, `description`) must precede all optional fields
- `metadata` follows `description` (4 skills currently use `metadata → name → description` — `cc-plugin`, `commit-tidy`, `fix`, `next`; `lint --fix` normalizes to `name → description → metadata`)
- `depends-on` follows `metadata` (or `description` directly when `metadata` is absent)
- `triggers` follows `depends-on`
- Optional fields should be in alphabetical order among themselves

### Valid Optional Fields

```yaml
agent: general-purpose     # Agent type
allowed-tools: [...]       # Tool restrictions
context: fork              # Context handling
depends-on: [skill-a, skill-b]  # Dependent skill list
hooks: {...}               # Hook configuration
model: claude-sonnet-4-... # Specific model
triggers: [...]            # Hook trigger declarations
user-invocable: true       # User can invoke directly
```

### Description Rules

- Max 1024 characters
- Include "what it does" + "when to use"
- Natural trigger keywords

## Workflow

### Step 0: External Validation (skills-ref CLI — Anthropic official)

Before applying the custom rules below, run Anthropic's official reference validator `skills-ref` if available. It enforces the upstream Agent Skills spec (name / description / frontmatter shape) — independent of the custom checks in this file.

#### 0a. Check availability

```bash
if command -v skills-ref >/dev/null 2>&1; then
  skills-ref --version
  SKILLS_REF_AVAILABLE=1
else
  SKILLS_REF_AVAILABLE=0
fi
```

#### 0b. Available — run validate

```bash
# Single skill
skills-ref validate ~/.claude/skills/<skill-name>

# All personal skills
for d in ~/.claude/skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  echo "=== $(basename "$d") ==="
  skills-ref validate "$d"
done
```

Treat any reported problem as a blocking issue. Re-run until the output is empty before proceeding to Step 1.

Properties readout (useful for cross-referencing the Topics table):

```bash
skills-ref read-properties ~/.claude/skills/<skill-name>   # JSON: name, description, ...
```

#### 0c. Not available — install

If `command -v uv` succeeds:

```bash
uv tool install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
```

After install, `skills-ref` is on PATH (`~/.local/bin/skills-ref`) — no alias needed. Re-run Step 0a to confirm, then 0b.

If `uv` is missing:

| Platform | Install uv |
|----------|------------|
| macOS | `brew install uv` |
| Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Windows (PowerShell) | `irm https://astral.sh/uv/install.ps1 \| iex` — runs in user scope, no elevation needed |

If neither `uv` nor a viable installer is available in the current environment, **skip Step 0 and proceed with Step 1** — the custom rules below provide partial coverage only (description-length budget, depends-on order, hardlink scan), not the upstream spec enforcement. **Report the skip explicitly** with a risk statement naming which upstream checks were not exercised (e.g., "Step 0 skipped — `skills-ref` name-match and properties-JSON validation not run").

#### 0d. Upgrade

```bash
uv tool upgrade skills-ref
```

#### Why both layers

| Validator | Strengths |
|-----------|-----------|
| `skills-ref` (upstream) | Authoritative spec enforcement (name match, description shape, properties JSON read) — tracks Anthropic's reference implementation |
| Custom rules (Steps 1–4 below) | Description length budget (1024), depends-on alphabetical order, hardlink-aware scan, plugin/project skill paths |

The two are complementary — run both. `skills-ref` failures must be fixed before the custom rules can be trusted.

### Step 1: Scan for Issues

```bash
# Missing required fields
find ~/.claude/skills -name "SKILL.md" ! -path "*.bak*" -exec sh -c \
  'head -10 "$1" | grep -q "^name:" || echo "name missing: $1"' _ {} \;

find ~/.claude/skills -name "SKILL.md" ! -path "*.bak*" -exec sh -c \
  'head -10 "$1" | grep -q "^description:" || echo "description missing: $1"' _ {} \;

# Invalid fields
grep -r "^triggers:" ~/.claude/skills --include="SKILL.md" | grep -v ".bak"
grep -r "^tools:" ~/.claude/skills --include="SKILL.md" | grep -v ".bak"

# Frontmatter position (must start on line 1)
find ~/.claude/skills -name "SKILL.md" ! -path "*.bak*" -exec sh -c \
  'head -1 "$1" | grep -q "^---$" || echo "frontmatter position error: $1"' _ {} \;
```

### Step 2: Report Issues

| File | Issue | Fix Required |
|------|-------|--------------|
| skill-a/SKILL.md | name: missing | Add name to frontmatter |
| skill-b/SKILL.md | triggers: used | Remove, add to description |
| skill-c/SKILL.md | tools: used | Change to allowed-tools: |

### Step 3: Fix (with user confirmation)

#### Missing Frontmatter

**Before:**
```markdown
# My Skill

Description here.
```

**After:**
```yaml
---
name: my-skill
description: Description here. "keyword1", "keyword2" triggers
---

# My Skill
```

#### triggers: → description

**Before:**
```yaml
---
name: my-skill
description: Does something useful
triggers:
  - keyword1
  - keyword2
---
```

**After:**
```yaml
---
name: my-skill
description: Does something useful. "keyword1", "keyword2" triggers
---
```

#### tools: → allowed-tools:

**Before:**
```yaml
tools:
  - Read
  - Bash(git:*)
```

**After:**
```yaml
allowed-tools: [Read, Bash(git:*)]
```

### Step 4: Validate

```bash
head -20 SKILL.md  # Check YAML syntax
```

## Dependency Validation (depends-on + external references)

### Step A: depends-on field validation

**Checks:**
1. Verify each listed skill actually exists
2. **Alphabetical order** — `[chezmoi, skill-manager, utcp]` (OK), `[utcp, chezmoi, skill-manager]` (NOT OK)

Auto-sort if not in alphabetical order:

```bash
# Extract depends-on from all SKILL.md → verify skill existence
# Handles BOTH inline (depends-on: [a, b]) AND block-style (depends-on:\n  - a\n  - b) YAML.
for skill_md in ~/.claude/skills/*/SKILL.md; do
  deps=$(awk '
    /^depends-on:[[:space:]]*\[/ { gsub(/^depends-on:[[:space:]]*\[|\]$|,/, " "); print; exit }
    /^depends-on:[[:space:]]*$/ { block=1; next }
    block && /^[[:space:]]+-[[:space:]]+/ { sub(/^[[:space:]]+-[[:space:]]+/, ""); printf "%s ", $0; next }
    block && /^[^[:space:]]/ { exit }
  ' "$skill_md")
  for dep in $deps; do
    dep=$(echo "$dep" | tr -d ' "'"'"'')
    [ -z "$dep" ] && continue
    if [ ! -d ~/.claude/skills/"$dep" ] && [ ! -d .claude/skills/"$dep" ]; then
      echo "BROKEN: $(dirname $skill_md | xargs basename) depends-on '$dep' — not found"
    fi
  done
done
```

### Step B: Skill reference validation in rules/PROMPT.md

Extract `/skill-name` or `Skill("skill-name"` patterns from rules, PROMPT.md, and skill topic files, then verify each referenced skill exists:

```bash
# Scan targets: ~/.agents/rules/*.md, .ralph/PROMPT.md, ~/.claude/skills/*/*.md
SCAN_PATHS="$HOME/.agents/rules/*.md .ralph/PROMPT.md $HOME/.claude/skills/*/*.md"

# /skill-name pattern (slash command references)
grep -hoP '(?<=/)[a-z][-a-z0-9]+' $SCAN_PATHS 2>/dev/null | sort -u | while read ref; do
  if [ ! -d ~/.claude/skills/"$ref" ] && [ ! -d .claude/skills/"$ref" ]; then
    echo "BROKEN_REF: /$ref — skill not found"
  fi
done

# Skill("name" pattern (Skill tool invocations)
grep -hoP 'Skill\("([^"]+)"' $SCAN_PATHS 2>/dev/null | sed 's/Skill("//;s/"//' | sort -u | while read ref; do
  if [ ! -d ~/.claude/skills/"$ref" ] && [ ! -d .claude/skills/"$ref" ]; then
    echo "BROKEN_REF: Skill(\"$ref\") — skill not found"
  fi
done
```

### Step C: Report format

| Source file | Reference | Status |
|-----------|------|------|
| `ralph/SKILL.md` | `depends-on: safe-delete` | OK / BROKEN |
| `rules/file-operations.md` | `/safe-delete` | OK / BROKEN |
| `.ralph/PROMPT.md` | `Skill("safe-delete")` | OK / BROKEN |

### Step D: Undeclared vendor-specific path coupling (HARD STOP)

Detect skill body references to vendor-specific paths/workflows that are NOT declared via `depends-on`. Undeclared coupling breaks portability — the skill silently assumes the vendor wrapper is present.

**Pattern**: a skill at `<scope>/skills/<X>/` references vendor paths like `.ralph/`, `.omc/`, vendor-named wrappers (`ralph improve`, `omc deploy`, etc.) without `depends-on` covering that vendor.

```bash
# Vendor paths: extend the regex as new wrappers are introduced.
# VENDOR_PAT escapes the leading dot so the bare `grep -nE "$VENDOR_PAT"` body scan matches `.ralph/` etc.
VENDOR_PAT='\.ralph/|\.omc/|\.codex/|\.ai/'

for skill_dir in ~/.claude/skills/*/ ~/.agents/skills/*/; do
  skill_name=$(basename "$skill_dir")
  skill_md="$skill_dir/SKILL.md"
  [ -f "$skill_md" ] || continue

  # Collect declared dependencies (handles BOTH inline `[a, b]` AND block-style YAML)
  declared=$(awk '
    /^depends-on:[[:space:]]*\[/ { gsub(/^depends-on:[[:space:]]*\[|\]$|,/, " "); print; exit }
    /^depends-on:[[:space:]]*$/ { block=1; next }
    block && /^[[:space:]]+-[[:space:]]+/ { sub(/^[[:space:]]+-[[:space:]]+/, ""); printf "%s ", $0; next }
    block && /^[^[:space:]]/ { exit }
  ' "$skill_md")

  # Scan body files for vendor patterns (SKIP SKILL.md — its depends-on is the declaration, not a body reference)
  for body in "$skill_dir"*.md; do
    [ "$(basename "$body")" = "SKILL.md" ] && continue
    matches=$(grep -nE "$VENDOR_PAT" "$body" 2>/dev/null | grep -v -E ':[[:space:]]*(#|//|<!--)')
    [ -z "$matches" ] && continue

    # Determine which vendor was hit (ralph / omc / codex / ai)
    while IFS= read -r line; do
      line_no=$(echo "$line" | cut -d: -f1)
      # Suppress when a sanitize/strip section header appears within the preceding 5 lines (informational, not structural).
      start=$(( line_no > 5 ? line_no - 5 : 1 ))
      if sed -n "${start},${line_no}p" "$body" | grep -qiE '^##.*(sanitize|strip|removal[[:space:]]+target)'; then
        continue
      fi
      # Drop the VENDOR_PAT leading `\.` and extract the vendor token directly.
      vendor=$(echo "$line" | grep -oE "$VENDOR_PAT" | head -1 | sed 's#^\.\([^/]*\)/$#\1#')
      [ -z "$vendor" ] && continue
      # If declared deps don't cover this vendor wrapper → BROKEN_COUPLING
      if ! echo "$declared" | grep -qw "$vendor"; then
        echo "BROKEN_COUPLING: $skill_name → $(basename $body) references $vendor without depends-on"
      fi
    done <<< "$matches"
  done
done
```

**Allowed exception (example/sanitize list)**: when the vendor reference appears in a "sanitize target list" (path enumeration to be **removed** before publishing) or example list, the coupling is informational, not structural. Detect by surrounding context (e.g., `## Sanitize`, `## Strip`, `removal target` headers within 5 lines above the match). Body matches outside such sections are flagged.

**Report row format**: append BROKEN_COUPLING entries to the Step C table.

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Hardcode `{workspace}/.ralph/fix_plan.md` path in a skill that does not declare `depends-on: ralph` | Use an abstract tracker reference (e.g., `<fix_plan tracker path>` per fix-plan SKILL.md `task-tracker` config). See fix-plan/SKILL.md "vendor-agnostic" note |
| 2 | Reference `ralph improve 5-A2` step from a non-Ralph-dependent skill | Generalize to "a post-hoc supervision flow" (or whichever abstract role the vendor instantiates) |
| 3 | Treat sanitize/strip lists as structural references | Sanitize/strip lists = informational; preserve as examples. Step D should NOT flag them |

## Related Actions

After lint completes, recommend:

### Duplicates Found?

If skills with similar names/descriptions exist:

```
💡 Found potential duplicates. Run dedup?
   /skill-manager dedup
```

### Multiple Related Skills?

If skills share a common prefix (e.g., `k8s-deploy`, `k8s-debug`):

```
💡 Related skills detected. Consider merging?
   /skill-manager merge k8s-deploy k8s-debug
```

## Auto-fix Rules

1. **triggers array → description string**
   - Convert to `"keyword1", "keyword2" triggers` format
   - Append to description

2. **tools → allowed-tools**
   - Rename field only, keep values

3. **Multi-line description cleanup**
   - Convert `|` block scalar to single line
   - Remove internal triggers: text

## Example

### Input (invalid)

```yaml
---
name: example-skill
description: |
  Example skill for demo
  triggers:
    - example
    - demo
tools:
  - Read
  - Edit
---
```

### Output (fixed)

```yaml
---
name: example-skill
description: Example skill for demo. "example", "demo" triggers
allowed-tools: [Read, Edit]
---
```

## Notes

- `.bak` directories are excluded from scans
- Always confirm before fixing
- For plugin skills, consider contributing fixes upstream
