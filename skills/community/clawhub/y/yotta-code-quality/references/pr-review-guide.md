# PR Review Guide — Mode 1

**Purpose:** Analyze a code diff or specific files for decay risks directly visible in the changed
code. Every finding must follow the Iron Law: Symptom → Source → Consequence → Remedy.

## Before You Start
- **Auto-generated files:** If the diff contains generated files (protobuf stubs, OpenAPI clients,
  ORM migrations, lock files, minified bundles), skip them entirely. Note which were skipped and why.
- **Scope calibration:** Adjust analysis depth by PR size before starting.

| PR Size | Approach |
|---------|----------|
| < 50 lines | Steps 1–3 only; Step 6a only if imports changed; Step 6b if any class/method/variable was renamed or introduced |
| 50–300 lines | Full process, all steps |
| > 300 lines | Full process; note in Scope that review is sampled — cover highest-risk areas, not every file |

For PRs > 500 lines: flag in the Summary that a PR this size is itself a Change Propagation signal.

## Analysis Process (work through in order, do not skip)

### Step 1: Understand the scope
- What is the stated purpose of this change? Which files were modified?
- Flag immediately if the PR changes > 10 unrelated files → 🟡 Warning: Change Propagation.

### Step 2: Scan for Change Propagation (R2) — first
- Does this change touch modules with no conceptual connection to the stated purpose?
- Does any modified class change for > 1 business reason?
- Does any method use more data from another class than its own?
- If no cross-module changes beyond what the feature requires → skip, no finding.

### Step 3: Scan for Cognitive Overload (R1)
- New/modified functions > 20 lines? Nesting > 3? > 4 params? Magic numbers? Unreadable names?
- Train-wreck chains (3+ calls chained)?

### Step 4: Scan for Knowledge Duplication (R3)
- Does this change introduce logic that already exists elsewhere?
- A new name for a concept that already has a name?
- A class added to a hierarchy that has a parallel in another module?

### Step 5: Scan for Accidental Complexity (R4)
- Abstraction with only one concrete use?
- A class that only wraps/delegates?
- Config options or extension points serving no current requirement?

### Step 6a: Scan for Dependency Disorder (R5)
- New imports from high-level module to low-level one (domain service imports DB driver/HTTP client)?
- New imports introducing a cycle between modules?
- An interface forcing callers to depend on methods they don't use?
- If no new imports/structural changes → skip, no finding.

### Step 6b: Scan for Domain Model Distortion (R6)
- New class/variable names match the business language?
- A new class holding only data with no behavior where behavior was expected?
- Logic that belongs to the domain placed in a service/utility layer?

## Severity Calibration
Apply the Iron Law format from `references/common.md`. Use `references/decay-risks.md` severity
guides as primary reference. Boundary tiebreaker:
- 🔴 Critical — actively breaking velocity or creating production risk *today*.
- 🟡 Warning — will if left unaddressed through the next few features.
- 🟢 Suggestion — worth fixing when nearby, not urgent.
If > 5 findings, add a one-line "Recommended fix order" at the end of Findings.

## Step 7: Quick Test Check (run last; three signals only)
Skip entirely if the diff contains only generated files, config, or docs with no production logic.

**Signal 1: Do tests exist for the changed behavior?**
- Diff modifies production code but no corresponding test changes included → 🟡 Warning: Coverage Illusion (Feathers — Working Effectively with Legacy Code, Ch. 1).
- Pure refactor with existing tests covering behavior → no finding.

**Signal 2: Quick Mock Abuse sniff** (only if diff includes test changes)
- Mock setup obviously longer than test logic? Primary assertions `expect(mock).toHaveBeenCalledWith(...)` with no behavior verification? Production methods added only for tests?
- If yes → 🟡 Warning: Mock Abuse (Osherove — The Art of Unit Testing).

**Signal 3: Quick Test Obscurity sniff** (only if diff includes test changes)
- Test names express scenario and expected outcome? Assertions have message strings?
- If vague/no messages → 🟢 Suggestion: Test Obscurity (Meszaros — xUnit Test Patterns, Assertion Roulette p.224).

**Output rule:** If all three signals clean → no Test findings, proceed to report. If findings exist →
add them in Iron Law format, labeled with the test risk name. Note in Summary: "Consider a full
test-quality review for systemic test problems."

## Step 8 (optional): Release / first-paint skim

When the user asked for a ship gate, or the diff touches updater, CSP, signing, publish scripts,
DevTools features, splash/loading, or license/status labels:

- Skim `editorial-extensions.md` (R7, UX1).
- Do not expand into a full Architecture audit unless asked.

## Output
Use the standard Report Template from `references/common.md`.
Mode: PR Review. Scope: list files reviewed (excluding skipped generated files).
