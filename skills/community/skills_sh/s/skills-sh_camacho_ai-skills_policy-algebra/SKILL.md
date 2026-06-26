---
name: policy-algebra
description: "Use when a skill, plan, or rule file needs a frozen Starlark governance rule block generated, or an existing frozen block drift-checked against a candidate. Invoke explicitly — not for general rule discussion."
---

# /policy-algebra

Generates frozen, drift-checkable governance rules from thin intent strings (deep interview) or rich plan inputs (shallow confirmation). Produces fenced Starlark blocks callers can inject into downstream work, and exposes `--verify` for canonicalized drift detection.

## Invocation

```
/policy-algebra <target>                      # generate rules
/policy-algebra <target> --write <path>       # generate + persist raw block
/policy-algebra --verify <frozen> <candidate> # drift check
```

`<target>` is a readable file path (SHALLOW mode) or an intent string (DEEP mode).

## Adaptive input detection

```
if target is a readable file path:
    mode = SHALLOW
    input = read(target)
else:
    mode = DEEP
    input = target
```

## Deep flow

1. Construct framing prompt for `/grill-me`:

   > "Interview the user to extract rule invariants for:
   >     \<target prompt\>
   >
   > Focus questions on:
   >   - Scope: what artifacts/events/phases does this rule govern?
   >   - Invariants: what must always be true? what must never happen?
   >   - Variable holes: what changes between instances?
   >   - Combinators: are existing operators (+, diff, intersect, method calls)
   >     enough, or do we need new helpers?
   >   - Failure modes: what happens when a rule can't be satisfied?
   >
   > Return a structured list of predicates in natural language.
   > /policy-algebra will draft Starlark from your output."

2. Invoke `/grill-me` via the `Skill` tool with that prompt.
3. Capture `/grill-me`'s output as the invariant list.
4. Continue to drafting (step 5 of shallow flow).

## Shallow flow

1. Read file contents.
2. Scan for invariant declarations — headings like "Invariants", "Rules", "Constraints"; bullets with MUST / NEVER / ALWAYS; predicate-looking code blocks.
3. Extract those as the invariant list.
4. If extraction yields fewer than 2 invariants OR content is ambiguous: fall through to DEEP mode with the file contents as target.
5. Draft Starlark from the invariant list per `notation.md` conventions.
6. Pass draft to `/review` (no panel hint — `/review` assembles).
7. `/review` converges → frozen, OR caps → inherit `/review` escalation.

## Drafting conventions

Group by subject (DEFAULTS, then named functions); keep each function body to 5 lines or fewer; one prose comment per function; no mutation. See `notation.md` for the full ruleset.

## Freeze and return

After `/review` APPROVE, capture the exact Starlark text as the FROZEN block. Do **not** canonicalize at freeze time — canonicalization is a compare-time operation only, keeping freeze/return simple.

Output format:

```
ALGEBRA:
```starlark
<raw frozen starlark block, as /review approved>
```
REVIEW_ROUNDS: <n>
PANEL: <comma-separated reviewers>
STATUS: CONVERGED
FILE: <path>        (only when --write was used)
NOTE: <non-obvious decision>   (optional)
```

If `--write <path>` was supplied, write the raw Starlark block to that path and include `FILE: <path>` in the return block.

## `--verify` flow

1. Read both files.
2. Extract first ` ```starlark ` fenced block from each file.
3. Normalize both blocks (strip trailing whitespace, collapse blank lines, trim edges).
4. If equal → print `MATCH`, exit 0. Else → print `DRIFT` + unified diff, exit 1.

Use the following bash to verify drift — no external dependencies needed:

```bash
# policy-algebra verify — inline, no dependencies
# Usage: bash verify.sh <frozen_file> <candidate_file>
normalize() { sed 's/[[:space:]]*$//' | sed '/^$/d'; }
extract_starlark() { sed -n '/^```starlark/,/^```$/p' "$1" | sed '1d;$d'; }

FROZEN=$(extract_starlark "$1" | normalize)
CANDIDATE=$(extract_starlark "$2" | normalize)

if [ "$FROZEN" = "$CANDIDATE" ]; then
  echo "MATCH"
  exit 0
else
  echo "DRIFT"
  diff <(echo "$FROZEN") <(echo "$CANDIDATE")
  exit 1
fi
```

## Multiple-block behavior

When a file contains multiple ` ```starlark ` blocks, `extractAlgebra` silently uses the first. This is intentional — wrap your canonical rules in the first fenced block of any document.

## Failure modes

| Failure | Behavior |
|---|---|
| Target omitted | Error: "target required" |
| SHALLOW: file unreadable | Fall through to DEEP with path string as intent |
| SHALLOW: < 2 extractable invariants | Fall through to DEEP with file contents as intent |
| DEEP: `/grill-me` unavailable | Error: "deep interview requires /grill-me skill" |
| DEEP: user abandons interview | Inherit `/grill-me`'s exit behavior |
| Drafting produces empty Starlark | Error: "no invariants found to codify"; return invariant list |
| `/review` caps without convergence | Inherit `/review` escalation — no custom handling |
| `--write <path>` unwritable | Error with path; return inline result anyway |
| Either `--verify` path unreadable | Error with path, exit 2 |
| No ` ```starlark ` block | `NoAlgebraBlockError` with path, exit 2 |
| `canonicalize` throws | Error with stack, exit 3 |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | MATCH (verify) / SUCCESS (normal) |
| 1 | DRIFT (verify only) |
| 2 | Input error (missing file, bad args, `NoAlgebraBlockError`) |
| 3 | Internal error |

## Cross-tool notes

- **Claude Code**: invokes `/grill-me` (DEEP interview) and `/review`
  (panel convergence) via the `Skill` tool. Both exist as project-local
  skills under `.claude/skills/`.
- **Codex / Cursor**: the `Skill` tool is Claude-Code-only. Read the
  relevant skill files directly:
    - `.claude/skills/grill-me/SKILL.md` — for the interview procedure
    - `.claude/skills/review/SKILL.md` — for panel convergence
  Apply their procedures inline rather than invoking them as commands.
  The drafting, freeze, and `--verify` logic in this SKILL.md is
  tool-agnostic and works identically for Claude Code, Codex, and Cursor.
- **CLI (`--verify` path)** is runtime-agnostic: use the inline bash snippet
  in the `--verify` section above — no Node or pnpm required.

## Governance

This skill is self-hosted: its own rules are encoded as a frozen Starlark governance block.
Drift from these invariants is a bug. Verify with `/policy-algebra --verify`.

```starlark
# policy-algebra governance — self-hosted
# FROZEN — do not edit; regenerate via /policy-algebra

DEFAULTS = {
    "min_invariants": 2,
    "exit_codes": {"match": 0, "drift": 1, "input_error": 2, "internal_error": 3},
    "required_output_fields": ["ALGEBRA", "REVIEW_ROUNDS", "PANEL", "STATUS"],
    "converged_status": "CONVERGED",
}

# SELECT_MODE: file path → SHALLOW; intent string → DEEP.
def SELECT_MODE(target):
    if is_readable_file(target):
        return "SHALLOW"
    return "DEEP"

# SHALLOW_OR_DEEP: fall through to DEEP when extraction yields < min_invariants or is ambiguous.
def SHALLOW_OR_DEEP(invariants, ambiguous):
    if len(invariants) < DEFAULTS["min_invariants"] or ambiguous:
        return "DEEP"
    return "SHALLOW"

# EXTRACT_BLOCK: use first starlark fence only; multiple blocks → first wins.
def EXTRACT_BLOCK(fences):
    if len(fences) == 0:
        return None
    return fences[0]

# OUTPUT_VALID: output must carry all required fields; STATUS=CONVERGED only after review.
def OUTPUT_VALID(output, review_loop_passed):
    fields_present = all([f in output for f in DEFAULTS["required_output_fields"]])
    converged_ok = output.get("STATUS") != DEFAULTS["converged_status"] or review_loop_passed
    return fields_present and converged_ok

# VERIFY: canonicalize both blocks and compare; never modify source files.
def VERIFY(frozen_canon, candidate_canon):
    if frozen_canon == candidate_canon:
        return DEFAULTS["exit_codes"]["match"]
    return DEFAULTS["exit_codes"]["drift"]

# EXIT_CODE: map outcome strings to numeric codes.
def EXIT_CODE(outcome):
    return DEFAULTS["exit_codes"].get(outcome, DEFAULTS["exit_codes"]["internal_error"])
```
