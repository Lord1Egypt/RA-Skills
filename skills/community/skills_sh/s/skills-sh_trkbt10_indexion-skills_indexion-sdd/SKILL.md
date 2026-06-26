---
name: indexion-sdd
description: Generate SDD requirements from RFCs/specs and quantitatively verify implementation conformance. spec draft → spec align → spec verify → automated validation loop with codex/claude. Operate spec-to-impl drift gates as CI checks.
---

# indexion SDD (Spec-Driven Development)

Bridge indexion's quantitative spec alignment tools with SDD agent workflows (cc-sdd, codex, etc.).

Provides: RFC/document → SDD draft, spec↔impl drift detection, and a validation loop
that feeds indexion's quantitative results into agent-driven qualitative review.

## When to Use

- User wants to implement an RFC or specification as a library/package
- User asks to verify spec-to-implementation conformance
- User wants to set up a SDD project with cc-sdd + codex + indexion
- User says "run the SDD loop" or "validate against the spec"
- After `codex spec-impl` completes, to check for drift before merging

## Important

- **Set cc-sdd `--lang` to match the implementation language, not the
  spec language.** If code is in English, use `--lang en`. Mismatched
  languages break `spec align diff` vocabulary matching.

## Process: RFC → Implementation → Validation

### Step 0: Project Setup

```bash
# Create project directory
mkdir my-rfc-impl && cd my-rfc-impl

# Install cc-sdd for your agent — set lang to match the code language
npx cc-sdd@latest --codex-skills --lang en --yes   # codex (skills mode)
npx cc-sdd@latest --claude-skills --lang en --yes   # claude (skills mode)

# Initialize project (language-specific)
# e.g., cargo init, npm init, moon new, etc.

# Initialize git
git init && git add -A && git commit -m "init"
```

**Verify indexion is available** before proceeding. The drift gate
(Step 2.5) and validation loop (Step 3) depend on it:

```bash
indexion --version                       # must be installed
indexion kgf edges <any-source-file>     # must detect language and show edges
```

If `indexion` is not installed, install it first. If the KGF for your
spec format is not recognized, update `indexion` to a version that
includes it. See Step 2.7 for the fallback when this cannot be resolved.

### Step 1: Specification → SDD Draft (indexion)

Fetch the specification document (RFC, ISO standard, etc.) and prepare it:

```bash
# For RFC: save as markdown or .rfc.txt
indexion spec draft --output .kiro/specs/<feature>/requirements.md rfc_document.md

# For ISO/IEC standards: extract text from PDF with cleanup, then draft
python3 scripts/extract_iso_text.py spec.pdf <start_page> <end_page> spec.spec.txt
indexion spec draft --output .kiro/specs/<feature>/requirements.md spec.spec.txt

# Create spec.json (set requirements.generated=true, approved=true)
```

The output uses `### Requirement N:` and `#### N.M:` hierarchy matching
cc-sdd's expected ID format. The agent's `$kiro-spec-requirements` phase will
further refine into EARS format with acceptance criteria.

**Supported specification formats:**
| Format | Extension | KGF spec |
|--------|-----------|----------|
| RFC plaintext | `.rfc.txt` | `rfc-plaintext` |
| ISO/IEC technical document | `.spec.txt` | `technical-document` |
| Markdown (README, etc.) | `.md` | `markdown` |

### Step 1.5: Specification Fidelity Check (indexion)

After writing requirements, verify they cover the source specification:

```bash
# Check requirements ↔ original spec alignment
# (spec align now accepts document files as impl when no code files are found)
indexion spec align diff .kiro/specs/<feature>/requirements.md spec.spec.txt \
  --format markdown --threshold 0.3

# SPEC_ONLY items = requirements not covered by original spec
# DRIFTED items = requirements using different vocabulary from original spec
```

**Traceability chain:** `spec align` works between documents at the
same abstraction level. For full traceability, check each adjacent pair:

```bash
# 1. Source spec ↔ requirements (fidelity)
indexion spec align diff requirements.md source-spec.spec.txt --threshold 0.3
# 2. Requirements ↔ design (design coverage)
indexion spec align diff requirements.md design.md --threshold 0.3
# 3. Requirements ↔ implementation (impl coverage) — after $kiro-impl
indexion spec align diff requirements.md src/ --threshold 0.3
```

Do NOT align source spec directly against design or code — the vocabulary
spaces differ too much (normative spec language vs. software design vs.
code identifiers). Each hop bridges one abstraction gap.

**Semantic fidelity review (not automatable):**

`spec align` checks vocabulary overlap, but cannot detect requirements
that **invert** the source spec's intent while using the same vocabulary.
A common failure mode:

- Source spec: "The DCTDecode filter **shall decode** JPEG data into samples"
- Requirements draft: "For DCTDecode, the decoder **shall return** an error
  indicating the filter is not yet supported"

Both mention "DCTDecode", "filter", "shall" — vocabulary matches, so
`spec align` reports MATCHED. But the requirement says the opposite of
what the spec demands. This creates a hidden gap that only surfaces when
E2E tests fail (Step 2.9).

**After `spec draft` generates requirements, review for these patterns:**

- `"not yet supported"`, `"not implemented"`, `"placeholder"`, `"stub"`
  — these indicate the draft punted on a spec requirement
- `"shall return an error"` for something the source spec says `"shall
  decode/process/convert"` — intent inversion
- Requirements that group multiple spec features into a single "unsupported"
  bucket — each spec feature deserves its own requirement

Fix these before proceeding to Step 2. Leaving them creates a false sense
of spec conformance that only E2E testing can expose.

### Step 2: Agent SDD Phases (codex / claude)

cc-sdd v3+ uses skills mode (`$kiro-spec-*` commands).

**Non-interactive execution with indexion gates between phases:**

```bash
FEATURE=<feature>
SPEC_DIR=.kiro/specs/$FEATURE
REPORT_DIR=.indexion/sdd-reports/$FEATURE
mkdir -p $REPORT_DIR

# Helper: approve a phase in spec.json
approve() { jq --arg p "$1" '.approvals[$p].approved = true' $SPEC_DIR/spec.json > /tmp/spec.json && mv /tmp/spec.json $SPEC_DIR/spec.json; }

# --- Design ---
codex exec --full-auto --json -C . "\$kiro-spec-design $FEATURE -y" > $REPORT_DIR/design.jsonl
approve design
# Verify requirements ↔ design
indexion spec align diff $SPEC_DIR/requirements.md $SPEC_DIR/design.md \
  --format markdown --threshold 0.3 | tee $REPORT_DIR/req-design-align.md
git add $SPEC_DIR && git commit -m "spec: design for $FEATURE"

# --- Tasks ---
codex exec --full-auto --json -C . "\$kiro-spec-tasks $FEATURE -y" > $REPORT_DIR/tasks.jsonl
git add $SPEC_DIR && git commit -m "spec: tasks for $FEATURE"

# --- Impl Phase A: Types & Structures ---
# Phase A implements type definitions, error types, data structures,
# and public API surface. No logic implementations yet.
cat > $REPORT_DIR/impl-phase-a.md << 'PHASE_A_EOF'
## Context

You are implementing Phase A (Types & Structures) of the <FEATURE> feature.
Read `.kiro/specs/<FEATURE>/tasks.md` for task details and
`.kiro/specs/<FEATURE>/design.md` for the design.

## Phase A Scope

In this phase, implement ONLY:
- Public type definitions (structs, enums, type aliases)
- Error types
- Constants and configuration structures
- Public API function signatures with placeholder bodies
- Test scaffolding (test files with placeholder tests)

Do NOT implement:
- Parsing, conversion, or transformation logic
- Algorithm implementations
- Complex function bodies beyond trivial constructors/accessors

## Per-Task Drift Gate

After completing each task and committing, run:

```bash
indexion spec align diff .kiro/specs/<FEATURE>/requirements.md src/<pkg>/ --format markdown --threshold 0.3
indexion spec align status .kiro/specs/<FEATURE>/requirements.md src/<pkg>/ --threshold 0.3 --fail-on drifted
```

If DRIFTED items remain for the requirement your task addresses, fix them
(add spec vocabulary to public declaration doc comments) and re-commit.

When all tasks are done, `spec align status --fail-on drifted` must exit 0.

## Important

Commit your work after completing tasks. Do not leave changes uncommitted.
PHASE_A_EOF

sed -i '' "s/<FEATURE>/$FEATURE/g; s/<pkg>/$PKG/g" $REPORT_DIR/impl-phase-a.md

codex exec --full-auto --json -C . \
  "$(cat $REPORT_DIR/impl-phase-a.md)" > $REPORT_DIR/impl-phase-a.jsonl
# Wait for Phase A to complete before running the gate
indexion spec align status $SPEC_DIR/requirements.md src/$PKG/ \
  --threshold 0.3 --fail-on drifted
git add . && git commit -m "impl: Phase A types for $FEATURE"

# --- Impl Phase B: Logic & Algorithms ---
# Phase B implements actual processing logic. The Phase A types
# are already committed, so Phase B focuses on function bodies.
cat > $REPORT_DIR/impl-phase-b.md << 'PHASE_B_EOF'
## Context

You are implementing Phase B (Logic & Algorithms) of the <FEATURE> feature.
Phase A (type definitions) is already committed. Read the existing type
definitions in `src/<pkg>/` and the design in `.kiro/specs/<FEATURE>/design.md`.

## Phase B Scope

In this phase, implement:
- Parsing logic (readers, decoders, interpreters)
- Conversion and transformation algorithms
- Validation logic beyond basic type construction
- Integration between types (connecting readers to data structures)
- Complete test implementations with real assertions

Every requirement that describes processing, conversion, interpretation,
or validation MUST have a corresponding function implementation — not
just a type definition.

## SHALLOW Resolution Rule

SHALLOW is detected when a requirement matches a type definition in a file
that has no non-trivial function implementations (>4 lines). To resolve:

**Add functions to the SAME FILE where the type is defined.**

Do NOT put logic in a separate file — SHALLOW checks per-file. If a
type is defined in one file and its methods are in a different file,
the type's file still has no functions and triggers SHALLOW.

Examples of functions that resolve SHALLOW:
- A method on the type with >4 lines of logic (match arms, loops,
  validation, computation)
- A constructor that does non-trivial work (parsing, validation)

Examples that do NOT resolve SHALLOW (too trivial, ≤4 lines):
- A default constructor that just returns a struct literal
- A one-liner boolean accessor

## Per-Task Drift Gate (with shallow detection)

After completing each task and committing, run:

```bash
indexion spec align diff .kiro/specs/<FEATURE>/requirements.md src/<pkg>/ --format markdown --threshold 0.3
indexion spec align status .kiro/specs/<FEATURE>/requirements.md src/<pkg>/ --threshold 0.3 --fail-on any
```

The `--fail-on any` gate includes SHALLOW detection: if a requirement
matched only to type definitions with no function implementations in
the same file, it is flagged as SHALLOW. You must add function
implementations to resolve SHALLOW items.

If DRIFTED, SPEC_ONLY, or SHALLOW items remain, fix them before proceeding.

When all tasks are done, `spec align status --fail-on any` must exit 0
with Shallow: 0.

## Important

Commit your work after completing tasks. Do not leave changes uncommitted.
PHASE_B_EOF

sed -i '' "s/<FEATURE>/$FEATURE/g; s/<pkg>/$PKG/g" $REPORT_DIR/impl-phase-b.md

codex exec --full-auto --json -C . \
  "$(cat $REPORT_DIR/impl-phase-b.md)" > $REPORT_DIR/impl-phase-b.jsonl &
CODEX_PID=$!
```

**Monitor impl progress:**

```bash
# Real-time event stream
tail -f $REPORT_DIR/impl.jsonl | jq -r '
  if .type == "item.completed" and .item.type == "agent_message" then
    "MSG: " + (.item.text[:120])
  elif .type == "item.completed" and .item.type == "command_execution" then
    "CMD: " + (.item.command[:60]) + " -> " + (.item.exit_code|tostring)
  else empty end'

# Stall detection
ps -p $CODEX_PID -o cputime,%cpu
lsof -p $CODEX_PID 2>/dev/null | grep tcp

# Resume after interruption
codex exec resume --last
```

**Operational notes:**

- Always use `--json` with file redirect + `tail -f`. Piping through
  `| tail` suppresses all output until completion.
- For long prompts, write to a file and use `$(cat file.md)`. Shell
  HEREDOC with `$()` can cause stdin blocking.
- Use `/loop` (Claude Code) to poll `git log --oneline -1` + `ps`
  every 60-120s during long impl runs.

### Step 2.5: Per-Task Drift Gate (indexion)

After each `$kiro-impl` task commit, run spec alignment to verify the
task closed its corresponding requirement gap. Do NOT proceed to the
next task if the requirement addressed by the current task is still
DRIFTED, SPEC_ONLY, or SHALLOW.

**Phase A gate** (types only — SHALLOW is expected and tolerated):

```bash
indexion spec align status $SPEC_DIR/requirements.md src/ --threshold 0.3 --fail-on drifted
```

**Phase B gate** (logic — SHALLOW must be zero):

```bash
indexion spec align diff $SPEC_DIR/requirements.md src/ --format markdown --threshold 0.3
indexion spec align status $SPEC_DIR/requirements.md src/ --threshold 0.3 --fail-on any
```

**SHALLOW detection:** When a requirement matches only to type/struct/enum
declarations in a file that contains no non-trivial function implementations
(>4 lines), `spec align` classifies it as SHALLOW. This catches two patterns:

1. Codex writes type definitions to satisfy vocabulary matching but omits
   the actual processing logic that the requirement demands.
2. Codex adds logic in a **separate file** from the type definition.
   SHALLOW checks per-file, so a type in one file with methods only in
   another file still triggers SHALLOW on the type's file.

**Resolution:** Add methods to the same file where the type is defined.
Trivial functions (constructors, one-liner accessors ≤4 lines) do not
count. See Phase B prompt template for examples.

When including this gate in a Codex prompt, instruct the agent to run
these commands after each task commit and fix any flagged items before
proceeding. Example instruction block for the prompt:

```
After completing each task (commit), run:
  indexion spec align diff ... --threshold 0.3
  indexion spec align status ... --threshold 0.3 --fail-on any
If DRIFTED, SPEC_ONLY, or SHALLOW items remain for the requirement
your task addresses, fix them before moving to the next task.
- DRIFTED: add spec vocabulary to public declaration doc comments
- SPEC_ONLY: implement the missing requirement
- SHALLOW: add non-trivial function implementations (>4 lines) to the
  SAME FILE where the matched type is defined. Do not add logic in a
  separate file — SHALLOW checks per-file.
When all tasks are done, spec align status --fail-on any must exit 0
with Shallow: 0.
```

### Step 2.6: Phase B Iteration (SHALLOW Resolution Rounds)

Phase B rarely resolves all SHALLOW items in a single Codex session.
Common causes:
- Codex adds logic in a new file instead of the type definition file
- Codex adds trivial constructors/accessors (≤4 lines) that don't count
- New type definitions are added without corresponding logic

**Iteration protocol:**

After each Phase B session completes:

1. Run the SHALLOW audit:
   ```bash
   indexion spec align status $SPEC_DIR/requirements.md src/$PKG/ \
     --threshold 0.3 --fail-on shallow
   ```

2. If `Shallow: 0`, proceed to E2E verification (Step 2.9).

3. If SHALLOW > 0, identify the specific items:
   ```bash
   indexion spec align diff $SPEC_DIR/requirements.md src/$PKG/ \
     --format markdown --threshold 0.3 | grep SHALLOW
   ```

4. Write a targeted round prompt that:
   - Lists the remaining SHALLOW items explicitly
   - Names the exact files that need functions added
   - States the rule: **add functions to the same file as the type**
   - Specifies what methods to add (not just "fix SHALLOW")

5. Launch the next round:
   ```bash
   codex exec --full-auto --json -C . \
     "$(cat $REPORT_DIR/round-N.md)" > $REPORT_DIR/round-N.jsonl &
   ```

**Typical: 2-3 rounds.** Round 1 adds core logic, Round 2 forces
same-file methods, Round 3 catches remaining edge cases.

### Step 2.7: Stall Detection and Recovery

Codex processes can stall (lost API connection, blocked review loop, etc.).
This is common during long Phase B sessions.

**Detection:**

```bash
# Check process vitals
ps -p $CODEX_PID -o cputime,%cpu,etime
lsof -p $CODEX_PID 2>/dev/null | grep tcp

# Stall indicators (all must be true):
# - CPU time not increasing over 2+ checks
# - 0.0% CPU
# - No TCP connections
# - JSONL event count not increasing
```

**Recovery — never commit manually:**

When a stall is confirmed:

1. Kill the process: `kill $CODEX_PID`
2. Check what was completed: `git log`, `git status`, `git diff --cached`
3. If uncommitted work exists and tests pass, generate indexion reports:
   ```bash
   indexion spec align diff $SPEC_DIR/requirements.md src/ \
     --format markdown --threshold 0.3 -o $REPORT_DIR/align-current.md
   indexion spec verify --spec="$SPEC_DIR/requirements.md" src/ \
     --format md -o $REPORT_DIR/verify-current.md
   ```
4. Write a resume prompt file that:
   - States which tasks are committed and which have uncommitted work
   - Includes the indexion reports as current-state evidence
   - Instructs Codex to verify and commit uncommitted work, then continue
   - Requires the per-task drift gate (Step 2.5) for all remaining tasks
5. Restart: `codex exec --full-auto --json -C . "$(cat $REPORT_DIR/resume-prompt.md)" > $REPORT_DIR/impl-resume.jsonl &`

**Never commit implementation code manually.** All commits must come from
the Codex agent. If you commit manually, you bypass the SDD protocol
(RED→GREEN evidence, review, verification) and invalidate the workflow.

### Step 2.8: Drift Gate Proxy (when Codex cannot run indexion)

Codex runs `indexion` commands inside the impl project directory. If
`indexion` is not installed, is too old, or lacks required KGF specs,
the drift gate commands will fail or timeout inside Codex.

**Prevention (recommended):** Verify in Step 0 that `indexion` works in
the project directory before starting the SDD run:

```bash
indexion --version
indexion kgf edges <any-project-file>   # should show edges, not errors
```

If `indexion` is not available or broken, install or update it first.

**Fallback — orchestrator-side drift gate:**

If `indexion` cannot be fixed before the run (e.g., a required KGF spec
is not yet released), the orchestrator runs the drift gate externally:

1. Tell Codex to skip drift gate commands in the impl prompt:
   ```
   The `indexion` binary is not available in this environment.
   Skip drift gate commands. The orchestrator will run them externally.
   ```
2. After each Codex commit, the orchestrator runs:
   ```bash
   indexion spec align diff $SPEC_DIR/requirements.md src/ \
     --format markdown --threshold 0.3
   indexion spec align status $SPEC_DIR/requirements.md src/ \
     --threshold 0.3 --fail-on any
   ```
3. If DRIFTED/SPEC_ONLY items appear, run the vocab fix step (Step 3.5)
   with the externally generated reports.

**`--specs-dir` caveat:** When running the indexion binary directly
(not via the project's build tool), it may not find KGF specs
automatically. Pass `--specs-dir` explicitly:

```bash
indexion spec align diff ... --specs-dir /path/to/indexion/kgfs
```

Without this, `spec align` may return "No alignment data found" because
the requirement document format is unrecognized.

### Step 2.9: E2E Verification (post-SHALLOW)

After all SHALLOW items are resolved (`Shallow: 0`), verify that the
implementation actually works end-to-end. `spec align` only checks
vocabulary — it cannot confirm functional correctness.

Write E2E tests that exercise the full pipeline against real input data:

```bash
# Example E2E pattern:
# 1. Load a real input file (not just synthetic fixtures)
# 2. Run the full processing pipeline end-to-end
# 3. Assert the output matches expected results
```

**Common E2E failure modes after SHALLOW=0:**
- Type definitions exist and logic functions exist, but the pipeline
  raises errors on real input (missing encoding tables, unsupported
  font types, etc.)
- All tests pass on synthetic fixtures but fail on real files because
  fixtures don't exercise the full code path
- Functions are implemented but not wired into the top-level API

If E2E tests fail, write additional Codex prompts targeting the specific
failure. The spec align gate ensures the vocabulary stays aligned while
Codex fixes the implementation.

### Step 2.10: Parallel Feature Execution

Multiple features can run in parallel Codex sessions:

```bash
for FEATURE in feature-a feature-b feature-c; do
  codex exec --full-auto --json -C . \
    "$(cat $REPORT_DIR/$FEATURE/impl-phase-b.md)" \
    > $REPORT_DIR/$FEATURE/impl-phase-b.jsonl 2>&1 &
  echo "$FEATURE: $!"
done
```

**Caveats:**
- Multiple Codex sessions may edit overlapping files (e.g., multiple
  features write to `src/graphics/`). Git will auto-merge unless the
  same lines are modified.
- If sessions commit in different branches, merge conflicts are the
  orchestrator's responsibility.
- Monitor all sessions with `/loop` — check event counts, commits,
  and process vitals for each PID.
- Stalls are more common with parallel sessions (API rate limits).
  Use Step 2.7 detection per-session.

### Step 3: Validation Loop (indexion + agent)

This is where indexion adds value beyond pure agent review.

```bash
# Quantitative analysis only (no agent)
indexion spec verify --spec='.kiro/specs/<feature>/requirements.md' src/lib/ --format md
indexion spec align diff .kiro/specs/<feature>/requirements.md src/lib/ --format markdown --threshold 0.3
indexion spec align status .kiro/specs/<feature>/requirements.md src/lib/ --threshold 0.3 --fail-on any

# Full loop: indexion quantitative + agent qualitative + auto-fix
./scripts/sdd-validate.sh <feature>           # validate only
./scripts/sdd-validate.sh <feature> --fix     # validate + auto-fix NO-GO tasks
```

The validation script:
1. Runs `spec verify` (vocabulary gap between spec and impl)
2. Runs `spec align diff` (requirement-level drift)
3. Runs `spec align trace` (traceability matrix)
4. Runs `spec align status` (CI-style pass/fail)
5. Injects all reports into the agent's `validate-impl` prompt
6. Agent produces GO/NO-GO decision with specific task numbers
7. On `--fix`, automatically re-runs `spec-impl` for failing tasks

### Step 3.5: Vocabulary Alignment Fix (indexion + agent)

After `$kiro-validate-impl` passes but `spec align` shows DRIFTED/SPEC_ONLY,
the implementation is functionally correct but lacks spec vocabulary in doc
comments. This step closes that gap.

**Note:** `$kiro-validate-impl` (cc-sdd) does not invoke indexion's spec align
internally. This step bridges the two tools.

```bash
# 1. Generate alignment reports
indexion spec align diff .kiro/specs/<feature>/requirements.md src/ \
  --format markdown --threshold 0.3 -o .indexion/sdd-reports/align-diff.md
indexion spec verify --spec='.kiro/specs/<feature>/requirements.md' src/ \
  --format md -o .indexion/sdd-reports/verify-gaps.md

# 2. Write a prompt file (avoid HEREDOC — use file to prevent stdin blocking)
cat > .indexion/sdd-reports/vocab-fix-prompt.md << 'EOF'
The spec alignment tool reports that several requirements are DRIFTED,
SPEC_ONLY, or SHALLOW. For each item, determine whether it is:

1. **Implementation gap** (SPEC_ONLY) — the spec requirement is not
   implemented at all. Add the missing implementation and tests.
2. **Vocabulary gap** (DRIFTED) — the implementation exists but spec
   vocabulary is missing from public doc comments. Add spec terms to
   public declarations.
3. **Depth gap** (SHALLOW) — the requirement matched to type definitions
   only, with no function implementations in the same file. Add the
   actual processing/parsing/conversion logic that the requirement demands.

Your task:
- Read the alignment report below.
- For each DRIFTED or SPEC_ONLY requirement, search the codebase for
  related keywords from that requirement. If related code exists, it is
  a vocabulary gap — add doc comments. If no related code exists, it is
  an implementation gap — implement it.
- The alignment tool only extracts vocabulary from public declarations.
  Doc comments on private functions are invisible to the tool.
- Run the project's formatter and test suite after editing.
- Commit your changes. Do not leave changes uncommitted.

## Spec Align Diff Report
EOF
cat .indexion/sdd-reports/align-diff.md >> .indexion/sdd-reports/vocab-fix-prompt.md
echo -e "\n## Vocabulary Gap Report" >> .indexion/sdd-reports/vocab-fix-prompt.md
head -40 .indexion/sdd-reports/verify-gaps.md >> .indexion/sdd-reports/vocab-fix-prompt.md

# 3. Run agent with the prompt file
codex exec --full-auto --json -C . \
  "$(cat .indexion/sdd-reports/vocab-fix-prompt.md)" \
  > .indexion/sdd-reports/vocab-fix.jsonl &

# 4. Monitor (optional)
tail -f .indexion/sdd-reports/vocab-fix.jsonl | jq -r '
  if .type == "item.completed" and .item.type == "agent_message"
  then "MSG: " + (.item.text[:120])
  elif .type == "item.completed" and .item.type == "command_execution"
  then "CMD: " + (.item.command[:50]) + " -> " + (.item.exit_code|tostring)
  else empty end'

# 5. Re-check alignment after agent completes
indexion spec align status .kiro/specs/<feature>/requirements.md src/ \
  --threshold 0.3 --fail-on any
```

**Key constraints:**
- The prompt does NOT dictate specific vocabulary to add. It provides the
  alignment reports and lets the agent determine what to fix.
- The agent must target public declarations only — private function doc
  comments are invisible to `spec align`.
- Typical: 1-2 fix cycles. If SPEC_ONLY persists, the agent may need
  guidance that the relevant public API entry point should carry the
  vocabulary (e.g. a top-level `open` function documents the full flow).

**Known blind spots:**

- **CLI entry points with no public API:** Main/entry-point modules
  often have no public declarations — all functions are private to the
  module. `spec align` extracts vocabulary only from public declarations,
  so entry-point modules always show Matched: 0 / SPEC_ONLY for all
  requirements. **Workaround:** split CLI logic into a library module
  that exposes public functions, with the entry point as a thin
  dispatcher. Align requirements against the library, not the entry point.

- **Empty doc comments:** Codex often writes doc comment syntax without
  any actual text content. These are invisible to `spec align` because
  they contain no vocabulary. The vocab fix prompt must explicitly
  instruct the agent: "Do not leave doc comments empty. Every public
  declaration must have a doc comment that describes its purpose using
  terminology from the requirements."

- **Internal-only modules (private functions):** When implementation
  logic is entirely private (not public), `spec align` cannot see it.
  This is common in filter/codec packages where a public pipeline
  function dispatches to private decoders. SHALLOW triggers on the
  type file even though logic exists. **Workaround:** either promote
  key internal functions to public (they become testable API surface),
  or consolidate spec vocabulary into the public pipeline function's
  doc comment so the requirement matches there instead.

- **Literal requirements vs. identifier matching:** Requirements that
  reference project-specific literals (package names, table numbers,
  configuration keys) will show as DRIFTED if the implementation doc
  comments don't mention the exact literal. This is usually a sign
  that the **requirements contain project-specific details that don't
  belong there** — fix the requirements to use generic descriptions,
  or accept that the vocab fix agent must propagate these literals.

- **"Fallback" framing vs. spec-mandated implementation:** When the
  agent proposes a "fallback" for an unsupported feature, verify
  whether the feature is actually required by the source specification.
  Example: TrueType font cmap table parsing was proposed as a
  "fallback" but is in fact mandated by the spec for TrueType font
  encoding resolution. Framing spec requirements as fallbacks creates
  incorrect priority and may lead to incomplete implementation.

- **Vocabulary match ≠ functional correctness:** DRIFTED=0 and
  SHALLOW=0 confirm vocabulary alignment but cannot verify that the
  implementation actually works. E2E tests (text extraction from real
  files, visual rendering comparison) are essential to catch:
  - Type definitions that compile but never execute
  - Processing pipelines that raise errors on real input
  - Coordinate transforms that produce wrong output
  - Font/encoding paths that silently return empty results

### Step 4: Documentation Drift Detection (plan reconcile)

After implementation, use `plan reconcile` to detect drift between
implementation code and its documentation (README, doc comments, etc.):

```bash
# Detect impl ↔ documentation drift
indexion plan reconcile --format md src/lib/

# Restrict to specific docs
indexion plan reconcile --format md --doc 'README.md' src/lib/
```

`plan reconcile` complements `spec align` in the SDD workflow:
- **spec align**: requirements.md ↔ implementation code (spec conformance)
- **plan reconcile**: implementation code ↔ documentation (doc freshness)

Use `spec align` for pre-merge gates (CI). Use `plan reconcile` for
ongoing documentation maintenance after the feature ships.

### Step 5: Visual E2E Verification (pixel diff)

For projects that produce visual output (PDF rendering, SVG export,
image processing), vocabulary-based spec align is insufficient.
Add pixel-level comparison against reference renderings.

**Pipeline:**
1. Generate output from the library (e.g., `pdf svg input.pdf output.svg`)
2. Rasterize to PNG at a fixed DPI (`rsvg-convert`, `puppeteer`, etc.)
3. Generate reference PNG from an established tool (`pdftoppm`, etc.)
4. Compare with `pixelmatch` — report diff percentage

**Thresholds:**
- < 0.01%: pixel-perfect (font AA differences only)
- < 0.1%: minor glyph positioning differences
- < 1%: visible text drift or image placement issues
- > 1%: structural rendering failure

**Iterative improvement:** Visual precision requires multiple rounds.
Each round fixes one category (font mapping → glyph positioning →
image CTM → colour conversion). Track all PDFs per round to catch
regressions — fixing one PDF must not break another.

**Known limitations of visual diff:**
- Font antialiasing differs between rasterizers (rsvg-convert vs pdftoppm)
- Sub-pixel rendering is platform-dependent
- 0.01% may be the practical floor for cross-rasterizer comparison

## Individual Commands

### spec draft — RFC/Document → SDD Requirements Draft

```bash
indexion spec draft <source-file-or-dir>
indexion spec draft --output requirements.md --format markdown rfc.md
indexion spec draft --profile sdd-requirement rfc.md
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output, -o` | stdout | Output file path |
| `--format` | markdown | Output format: markdown, json |
| `--profile` | sdd-requirement | Draft profile (KGF spec name) |
| `--max-requirements` | 64 | Maximum requirements to extract |
| `--specs-dir` | auto | KGF specs directory |

### spec verify — Vocabulary Gap Check

```bash
indexion spec verify --spec='requirements.md' src/lib/ --format md
```

| Option | Default | Description |
|--------|---------|-------------|
| `--spec` | (required) | Spec document glob (repeatable) |
| `--format` | json | Output format: json, md, github-issue |
| `--focus` | all | Token kind filter: ident, text, vocab, all |
| `--max-candidates` | 200 | Maximum items in output |
| `-o, --output` | stdout | Output file path |

### spec align diff — Requirement-Level Drift

```bash
indexion spec align diff requirements.md src/lib/ --format markdown --threshold 0.3
```

Reports: MATCHED, DRIFTED, SPEC_ONLY (spec with no impl match), IMPL_ONLY (impl with no spec match), SHALLOW (matched to type-only stubs without function implementations).

### spec align trace — Traceability Matrix

```bash
indexion spec align trace requirements.md src/lib/ --format json --threshold 0.3
```

Generates requirement → implementation mapping for auditing.

### spec align status — CI Gate

```bash
indexion spec align status requirements.md src/lib/ --fail-on any --threshold 0.3
# Exit code non-zero on failure when used with --fail-on
```

| `--fail-on` | Description |
|-------------|-------------|
| `none` | Always pass |
| `drifted` | Fail if any DRIFTED |
| `spec-only` | Fail if any SPEC_ONLY |
| `shallow` | Fail if any SHALLOW (type-only stubs without function implementations) |
| `any` | Fail on DRIFTED, SPEC_ONLY, SHALLOW, or CONFLICT |

### spec align watch — Watch Mode

```bash
indexion spec align watch --mode=diff requirements.md src/lib/
indexion spec align watch --mode=status requirements.md src/lib/
```

Reruns alignment when spec or implementation inputs change.

### spec align suggest — Reconciliation Suggestions

```bash
indexion spec align suggest requirements.md src/lib/ --format tasks --agent codex
```

Generates actionable suggestions to close spec↔impl gaps.

## Threshold

Use `--threshold 0.3` for SDD alignment commands. The default `0.6` is
too high because SDD acceptance criteria are short text matched against
code + doc comments, not full-document similarity.

## Multi-Language Support

The SDD pipeline works with any language that has a KGF spec.

### KGF Requirements for SDD

For spec align to work, the language's KGF must:
1. **Capture doc comments in declares edges** — `doc` must be non-empty
2. **Use correct PEG alternative ordering** — DocComment must be after
   declaration rules in the Item alternatives
3. **Handle NL between doc and keyword** — `NL?` or `NL*` after `doc:DocComment?`

Verify with: `indexion kgf edges <file>` — if declares edges lack `doc=`,
the KGF needs fixing.
