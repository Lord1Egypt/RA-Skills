# Anti-Patterns — skill-scorer

> A checklist of common skill mistakes. Use this during Step 3 (Issue Identification).
> Each anti-pattern maps to a scoring dimension and has a detection method.

---

## Category A: Metadata & Triggering Failures

### A1. Missing YAML Frontmatter
**Detect:** No `---` delimited block at top of SKILL.md.
**Severity:** 🔴 Critical
**Impact:** Skill will never be discovered or triggered. Name and description are invisible to the agent.
**Fix:** Add frontmatter with at least `name` and `description`.

### A2. Vague Description
**Detect:** Description is under 20 words, uses only generic terms ("a helpful skill for tasks"), or lacks specific trigger contexts.
**Severity:** 🟡 Warning
**Impact:** Severe undertriggering. Claude won't choose this skill over alternatives.
**Fix:** Make description specific: include what the skill does, when to use it, and example trigger phrases. Be "pushy" — explicitly list contexts.

### A3. Cryptic Name
**Detect:** Name uses abbreviations (`srch-flt-v2`), internal codes (`proj-tempest-gen`), or version suffixes.
**Severity:** 🟡 Warning
**Impact:** Hard for users to discover via slash command. Hard for Claude to match semantically.
**Fix:** Use descriptive verb-noun or gerund form: `search-cheap-flights`, `generating-reports`.

### A4. No Anti-Trigger Guidance
**Detect:** No "Do NOT activate for" or "Don't use when" section.
**Severity:** 🟢 Suggestion
**Impact:** May overtrigger for related but incorrect use cases, especially if sibling skills exist.
**Fix:** Add explicit anti-triggers: "Do NOT activate for X → use skill-Y instead."

---

## Category B: Structure & Architecture Failures

### B1. Monolithic SKILL.md (>500 lines)
**Detect:** SKILL.md exceeds 500 lines without references.
**Severity:** 🟡 Warning
**Impact:** Floods the context window. Claude may lose track of instructions in a long context.
**Fix:** Extract domain knowledge, large examples, and lookup tables into `references/` files. Keep SKILL.md as the routing and workflow hub.

### B2. No Progressive Disclosure
**Detect:** All content is in SKILL.md with no references. Or references exist but SKILL.md doesn't specify when to load them.
**Severity:** 🟡 Warning
**Impact:** Wastes context tokens on information not needed for most requests.
**Fix:** Add a References table at the bottom of SKILL.md specifying each file's purpose and when to read it.

### B3. Deeply Nested References
**Detect:** A reference file references another reference file, creating a chain (references/a.md → references/b.md → references/c.md).
**Severity:** 🟡 Warning
**Impact:** Claude may fail to follow multi-hop chains, losing critical information.
**Fix:** Flatten references to max 2 levels: SKILL.md → references/X.md. No reference file should reference another.

### B4. External Path References
**Detect:** File references paths outside the skill folder (../../shared/, /global/, absolute paths).
**Severity:** 🔴 Critical
**Impact:** Skill breaks when uploaded to a different location or shared with others.
**Fix:** Copy all shared files into the skill's own directory. Each skill must be a self-contained unit.

---

## Category C: Instruction Quality Failures

### C1. Passive Voice Instructions
**Detect:** Frequent use of "should be done", "it is recommended that", "one might consider".
**Severity:** 🟢 Suggestion
**Impact:** Ambiguous instructions lead to inconsistent behavior.
**Fix:** Use imperative form: "Do X", "Use Y", "Always Z". Explain why after the instruction.

### C2. No Examples
**Detect:** Workflow or output format described in abstract terms with zero concrete examples.
**Severity:** 🟡 Warning
**Impact:** Claude must guess at the intended output format, leading to inconsistent results.
**Fix:** Add 1-3 input/output examples using realistic data. Use "Example:" blocks.

### C3. Contradictory Instructions
**Detect:** Two sections give conflicting guidance (e.g., "always include X" vs "never include X").
**Severity:** 🔴 Critical
**Impact:** Claude picks whichever instruction it encounters last, leading to unpredictable behavior.
**Fix:** Audit all instructions for consistency. Use a single source of truth for each rule.

### C4. Over-Constrained (Zero Degrees of Freedom)
**Detect:** Every single step is rigidly prescribed with no room for Claude to adapt.
**Severity:** 🟢 Suggestion
**Impact:** Skill breaks when encountering any scenario not explicitly covered.
**Fix:** Constrain outputs and safety-critical steps tightly. Give Claude freedom on approach and ordering where appropriate.

### C5. Teaching Claude What It Already Knows
**Detect:** Long explanations of basic concepts (what JSON is, how HTTP works, what an API is).
**Severity:** 🟡 Warning
**Impact:** Wastes context tokens and dilutes important instructions.
**Fix:** Remove explanations of common knowledge. Add only what Claude genuinely doesn't know (project-specific conventions, custom formats, domain mappings).

---

## Category D: Workflow & Logic Failures

### D1. Missing Workflow Steps
**Detect:** Skill describes desired output but doesn't define the steps to get there.
**Severity:** 🔴 Critical
**Impact:** Claude must improvise the entire execution path.
**Fix:** Define a numbered step sequence from input to output. Each step should have clear inputs and outputs.

### D2. No Output Validation
**Detect:** Workflow ends at "format output" with no self-check or quality gate.
**Severity:** 🟡 Warning
**Impact:** Claude may deliver outputs missing required elements (links, tags, formatting).
**Fix:** Add a final "Validate Output" step with a checklist of required elements.

### D3. Unrealistic Examples
**Detect:** Examples use placeholder data ("example.com", "John Doe", "2020-01-01") instead of realistic values.
**Severity:** 🟢 Suggestion
**Impact:** Harder for Claude to understand the expected output format in real-world context.
**Fix:** Use realistic but anonymized data: real city names, future dates, plausible IDs.

### D4. No Ambiguity Handling
**Detect:** Skill assumes user input is always complete and unambiguous. No clarification prompts defined.
**Severity:** 🟡 Warning
**Impact:** Claude either guesses (wrong) or stalls (unhelpful) on incomplete input.
**Fix:** Define parameter collection strategy: what to ask for, defaults for optional params, max questions per round.

---

## Category E: Error Handling Failures

### E1. No Fallback Paths
**Detect:** No fallback, error, or "what if" section exists.
**Severity:** 🟡 Warning (🔴 Critical for CLI-wrapping skills)
**Impact:** On failure, Claude either hallucinates an answer or silently stops.
**Fix:** Define at least: tool not available, no results, invalid input, timeout/network error.

### E2. Hallucination on Failure
**Detect:** Skill's implicit behavior on failure would be to answer from training data (no "do NOT use training data" guard).
**Severity:** 🔴 Critical (for CLI/API skills)
**Impact:** User receives fabricated data presented as real results.
**Fix:** Add explicit guard: "If [tool] fails, report the error honestly. Do NOT substitute training data."

### E3. Missing Environment Check
**Detect:** Skill depends on external tools (CLI, API, packages) but has no Step 0 verification.
**Severity:** 🟡 Warning
**Impact:** Skill fails mid-execution when dependency is missing, without a clear error message.
**Fix:** Add Step 0: check dependency → install if missing → verify → STOP if still missing.

---

## Category F: Context Efficiency Failures

### F1. Redundant Content
**Detect:** Same instruction or concept appears in 2+ places within the skill.
**Severity:** 🟢 Suggestion
**Impact:** Wastes context tokens. Risks contradictions if one copy is updated but not the other.
**Fix:** Say it once, in the most logical place. Reference it from elsewhere if needed.

### F2. Domain Knowledge in SKILL.md
**Detect:** SKILL.md contains large lookup tables, city lists, category mappings, or similar data blocks.
**Severity:** 🟡 Warning
**Impact:** Loaded into context even for queries that don't need this data.
**Fix:** Move data to `references/` files. Load on demand with clear guidance in the References table.

### F3. Verbose Metadata
**Detect:** Name + description combined exceed ~150 tokens.
**Severity:** 🟢 Suggestion
**Impact:** Every conversation pays this cost, even when the skill isn't triggered.
**Fix:** Keep name under 5 words. Keep description under 100 words. Move details to SKILL.md body.

---

## Category G: Portability & Compatibility Failures

### G1. Hardcoded Paths
**Detect:** Absolute paths or user-specific paths in skill content (/Users/alice/, C:\Users\bob\).
**Severity:** 🔴 Critical
**Impact:** Skill breaks for anyone except the original author.
**Fix:** Use relative paths within the skill folder, or environment variables.

### G2. No Dependency Declaration
**Detect:** Skill uses external tools but never lists them or provides install instructions.
**Severity:** 🟡 Warning
**Impact:** User doesn't know what to install. Claude can't recover if dependency is missing.
**Fix:** Add a Prerequisites section with install commands and version requirements.

### G3. Platform-Specific Assumptions
**Detect:** Skill assumes a specific OS, shell, or agent platform without declaring it.
**Severity:** 🟢 Suggestion
**Impact:** May fail silently on different platforms.
**Fix:** Add `compatibility` field to frontmatter. Handle platform differences in workflow (if/else on OS).

---

## Category H: Safety & Robustness Failures

### H1. Knowledge as Primary Data Source (CLI/API skills)
**Detect:** Large Domain Knowledge section with directly-usable answers (specific prices, hotel names, flight routes).
**Severity:** 🟡 Warning
**Impact:** Claude may answer from knowledge instead of executing the CLI, giving stale data.
**Fix:** Knowledge should contain mappings (intent → param), not answers. Add disclaimer: "does NOT replace execution."

### H2. No Identity Lock (CLI/API skills)
**Detect:** CLI-wrapping skill has no "CRITICAL EXECUTION RULES" or equivalent guard at the top.
**Severity:** 🟡 Warning
**Impact:** Claude treats the skill as a knowledge base rather than an execution guide.
**Fix:** Add identity lock block immediately after frontmatter.

### H3. Fabricated Parameters
**Detect:** Skill uses CLI flags or API parameters not listed in parent tool's documentation.
**Severity:** 🔴 Critical
**Impact:** Commands will fail. User loses trust.
**Fix:** Cross-validate every parameter against the tool's --help or official docs. Remove fabricated ones.

### H4. Unsanitized User Input in Commands
**Detect:** User input is directly interpolated into shell commands or code without any escaping.
**Severity:** 🟡 Warning
**Impact:** Potential injection vector if skill is used in automated pipelines.
**Fix:** Use proper quoting and escaping. Note: in most SKILL.md contexts, Claude handles this naturally, but explicit guidance helps.

---

## Quick Detection Checklist

Use this as a rapid scan before deep evaluation:

```
[ ] Frontmatter exists with name + description?
[ ] Description > 20 words and includes trigger contexts?
[ ] SKILL.md < 500 lines?
[ ] At least 1 concrete example in the workflow?
[ ] Error handling / fallback section exists?
[ ] No external path references?
[ ] References table exists (if reference files exist)?
[ ] No large data tables in SKILL.md body?
[ ] Dependencies declared (if any)?
[ ] Output validation step exists?
```
