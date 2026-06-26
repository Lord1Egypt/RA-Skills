# Scoring Rubric — skill-scorer

> This rubric defines the exact criteria for each of the 8 evaluation dimensions.
> Each dimension is scored 0–100. The final score is a weighted average.

---

## Dimension 1: Metadata & Triggering (Weight: 15%)

Evaluates whether Claude can **discover and correctly activate** this skill.

### Scoring Criteria

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-20 | **YAML frontmatter exists** with `name` and `description` | Parse the `---` block at top of SKILL.md |
| 0-20 | **Name follows conventions** — descriptive, uses gerund or verb-noun form, no cryptic abbreviations | Check: would a user or LLM understand what this skill does from the name alone? |
| 0-30 | **Description is effective** — specific enough to trigger correctly, broad enough to catch edge queries, includes anti-trigger guidance | Test: given 5 hypothetical user queries, would this description cause correct triggering? |
| 0-15 | **Description is "pushy" enough** — addresses undertriggering by being explicit about when to activate | Check: does description say "use when..." or "triggers on..." with concrete examples? |
| 0-15 | **Trigger section in body** (if present) — complements description with explicit trigger phrases and anti-triggers | Check for "When to Activate" / "Do NOT activate for" sections |

### Scoring Guide

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Description alone would reliably trigger for all intended use cases. Name is intuitive. Anti-triggers defined. |
| 70-89 | Description covers main use cases but misses edge cases. Name is clear. |
| 50-69 | Description is vague or too narrow. May undertrigger or overtrigger. |
| 30-49 | Description is a generic sentence. Name is cryptic. Claude would rarely choose this skill. |
| 0-29 | Missing frontmatter, no description, or name is meaningless. |

---

## Dimension 2: Structure & Architecture (Weight: 15%)

Evaluates the **file organization and information architecture** of the skill.

### Scoring Criteria

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-20 | **SKILL.md is the entry point** — contains the core logic, not just a pointer to other files | Check that the main workflow is in SKILL.md, not buried in references |
| 0-20 | **Progressive disclosure** — 3-level loading: metadata (always) → SKILL.md body (on trigger) → references (on demand) | Check: are references clearly separated? Does SKILL.md tell Claude when to read each reference? |
| 0-15 | **SKILL.md length is appropriate** — ideally under 500 lines; if longer, must justify with complexity | Count lines. Under 200 = good. 200-500 = acceptable. Over 500 = needs splitting. |
| 0-15 | **Logical section ordering** — follows a natural flow (overview → when → how → output → references) | Check section sequence for coherence |
| 0-15 | **Reference files are well-organized** — clear naming, each file has a single purpose, SKILL.md has a reference table | Check references/ directory structure and the References section in SKILL.md |
| 0-15 | **No deeply nested references** — reference files should not reference other reference files (max 2 levels) | Check for chains of file references |

### Scoring Guide

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Clean 3-level progressive disclosure. SKILL.md under 300 lines. All references clearly mapped. |
| 70-89 | Good structure with minor issues (e.g., slightly long SKILL.md, one unclear reference). |
| 50-69 | Flat structure (everything in SKILL.md) or messy reference organization. |
| 30-49 | No separation of concerns. SKILL.md is a wall of text with no references. |
| 0-29 | Chaotic structure. Missing files. No logical organization. |

---

## Dimension 3: Instruction Clarity (Weight: 15%)

Evaluates whether the instructions are **clear, actionable, and well-written**.

### Scoring Criteria

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-20 | **Uses imperative form** — "Do X" not "You should consider doing X" | Scan for weak modal verbs (should, could, might, consider) |
| 0-20 | **Explains WHY, not just WHAT** — gives reasoning behind rules so Claude can generalize | Check: are constraints accompanied by rationale? |
| 0-20 | **Includes concrete examples** — input/output pairs, before/after, or code samples | Count examples. 0 = bad. 2-3 = good. Excessive = bloat. |
| 0-15 | **Avoids redundancy** — no repeated instructions across sections | Check for duplicate or near-duplicate content |
| 0-15 | **Right degree of freedom** — tight constraints where precision matters, loose guidance where creativity helps | Assess: is every step locked down, or does the skill trust Claude where appropriate? |
| 0-10 | **Consistent terminology** — same concept uses same term throughout | Check for inconsistent naming of the same concept |

### Scoring Guide

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Every instruction is actionable. Examples are crisp. No redundancy. Perfect balance of prescriptive and permissive. |
| 70-89 | Clear overall, but some instructions are vague or redundant. Examples present. |
| 50-69 | Mix of clear and unclear instructions. Missing examples or excessive hand-waving. |
| 30-49 | Mostly vague or passive instructions. No examples. Claude would struggle to follow. |
| 0-29 | Incomprehensible, contradictory, or absent instructions. |

---

## Dimension 4: Workflow & Logic (Weight: 15%)

Evaluates the **operational correctness and completeness** of the skill's workflow.

### Step 0: Skill Type Detection (do this BEFORE scoring)

Different skill types have fundamentally different workflow patterns. Identify the type first, then apply the matching criteria.

| Type | How to Detect | Workflow Pattern |
|------|--------------|-----------------|
| **Instruction-only** | No CLI commands, no API calls, no scripts, no external tools. Pure markdown instructions. Examples: brand-guidelines, commit-formatter, code-review checklist | Rules/templates → Claude applies them using its own judgment |
| **Single-command executor** | One CLI/API command with scenario-specific defaults. SKILL.md contains the command template directly in workflow steps | Collect params → execute one command → format output |
| **Multi-command orchestration** | Multiple CLI/API commands combined. Parameters block defines a command pool; Playbooks describe how to combine them; Usage Examples give executable samples | Detect query type → select commands → orchestrate sequence → merge outputs |
| **Script-bundled** | Has a `scripts/` directory with executable code (Python/bash/Node). SKILL.md defines when and why; scripts handle the how. Claude invokes scripts and interprets their output | SKILL.md dispatches → script executes deterministic logic → Claude interprets results |
| **MCP-integrated** | Depends on an external MCP server connection. Skill is the "knowledge layer" on top of MCP tools — it tells Claude how to use those tools effectively | Verify MCP connection → call MCP tools per skill rules → format output following skill conventions |

**Critical rules:**
- An orchestration skill that puts executable commands in Parameters + Usage Examples and orchestration logic in Playbooks is a valid design pattern — not a workflow gap. Do NOT penalize it for "playbooks contain descriptive logic instead of executable commands."
- A script-bundled skill where SKILL.md is short and delegates to scripts is a valid design pattern — the workflow completeness lives in the scripts, not in SKILL.md. Evaluate the dispatch logic and script documentation, not SKILL.md line count.
- An MCP-integrated skill that says "use MCP tool X to do Y" without reimplementing the tool's logic is correct — the skill provides workflow guidance, not tool reimplementation.

### Scoring Criteria — Instruction-Only Skills

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-25 | **Rules are complete** — cover all relevant cases, no obvious gaps | Could Claude handle edge cases with these instructions alone? |
| 0-25 | **Output format defined** — templates, examples, or structure specified | Check for output templates or format examples |
| 0-25 | **Realistic examples** — input/output pairs demonstrate correct application | Check: do examples cover typical and edge cases? |
| 0-25 | **Handles ambiguous input** — guidance for unclear or borderline cases | Check for decision criteria or "when in doubt" guidance |

### Scoring Criteria — Single-Command Executor Skills

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-20 | **Complete workflow** — all steps from param collection to output delivery | Trace: can Claude handle a request end-to-end? |
| 0-20 | **Parameter handling** — required vs. optional clear; defaults specified; collection SOP defined | Check for parameter tables, defaults, collection strategy |
| 0-15 | **Validation step exists** — self-check before delivering results | Look for output validation / quality gate step |
| 0-15 | **Step dependencies clear** — each step knows what it receives from previous | Check data flow between steps |
| 0-15 | **Realistic usage examples** — commands that would actually work | Check: real values, future dates, valid IDs? |
| 0-15 | **Handles ambiguous input** — what to do when user intent is unclear | Check for clarification prompts or default behaviors |

### Scoring Criteria — Multi-Command Orchestration Skills

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-20 | **Command pool defined** — all available commands and their parameters are listed in a structured format (Parameters block or equivalent). This is where the "what can I call" lives | Check: are all CLI/API commands the skill can use clearly documented with flags and descriptions? A well-structured Parameters block = full score |
| 0-20 | **Orchestration logic defined** — Playbooks describe how to select and combine commands based on query type. Playbooks are EXPECTED to contain descriptive/procedural logic (e.g., "Step 1: search flights → Step 2: use result to search hotels"), NOT raw executable commands. The executable form lives in Usage Examples, not here | Check: do playbooks show command selection logic and sequencing? Different playbooks should have genuinely different command combinations. Score based on clarity of orchestration logic, not whether playbook text is directly copy-pasteable into a terminal |
| 0-15 | **Query type routing** — skill determines which subset of commands to run based on user intent (e.g., single-point query vs full itinerary) | Check: does Step 1 or equivalent classify the query before executing? |
| 0-15 | **Usage Examples are executable** — the Usage Examples section in SKILL.md contains concrete command samples with realistic parameters that can be copy-pasted and run. This is separate from Playbooks — playbooks describe logic, Usage Examples demonstrate concrete invocations | Check: does the Usage Examples section contain real `cli command --flag value` lines? Are values realistic (real cities, future dates)? |
| 0-15 | **Output merging logic** — how results from multiple commands are combined into a unified response. This can be defined in SKILL.md's Output Rules, in references/templates.md, or both. Any of these locations is valid | Check: is there a defined format (table, day-by-day, sections) for presenting multi-command results together? Location doesn't matter — existence and clarity do |
| 0-15 | **Validation step exists** — self-check covers all commands' outputs, not just the last one | Check: does validation verify booking links / data sources across all command results? |

### Scoring Criteria — Script-Bundled Skills

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-20 | **Dispatch logic clear** — SKILL.md tells Claude which script to run and when, with explicit invocation commands (e.g., `Run scripts/analyze.py --input {file}`) | Check: can Claude determine which script to call from SKILL.md instructions alone? |
| 0-20 | **Script documentation** — each script's purpose, inputs, outputs, and expected behavior are documented (in SKILL.md, script comments, or references/) | Check: could Claude understand what a script returns without reading its source code? |
| 0-15 | **Dependency declaration** — required packages, runtimes, and environment prerequisites are listed | Check for Prerequisites section or equivalent. Scripts that silently fail on missing dependencies are a critical flaw |
| 0-15 | **Error handling in dispatch** — SKILL.md defines what to do when a script fails (non-zero exit, unexpected output, timeout) | Check: is there a "if script fails → do X" path? |
| 0-15 | **Output interpretation** — SKILL.md tells Claude how to read and present script output to the user | Check: does the skill define how to parse script results (JSON, HTML, plaintext) and format them? |
| 0-15 | **Self-containment** — scripts are bundled in the skill folder, not referenced as external paths | Check: are all scripts in `scripts/` within the skill directory? No `../../shared/` references? |

### Scoring Criteria — MCP-Integrated Skills

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-20 | **MCP dependency declared** — skill explicitly states which MCP server(s) it requires and how to verify connectivity | Check for: MCP server name, connection verification step, "Requires X MCP server" in Prerequisites or frontmatter |
| 0-20 | **Tool usage guidance** — skill defines which MCP tools to use, in what order, and with what parameters for each workflow | Check: does the skill go beyond "use MCP tools" to specify which tools and how? |
| 0-15 | **Connection failure handling** — skill defines what to do when MCP server is disconnected or unreachable | Check for: "MCP not connected → tell user to reconnect. Do NOT proceed." Not just generic error handling |
| 0-15 | **Workflow adds value over raw MCP** — skill provides orchestration, formatting, or domain logic that raw MCP tool calls don't | Check: would removing the skill and using MCP tools directly produce the same result? If yes, the skill adds no value |
| 0-15 | **Output formatting rules** — skill defines how to present MCP tool results to the user | Check: does the skill specify output structure, not just pass through raw MCP responses? |
| 0-15 | **Realistic usage examples** — examples show complete MCP-mediated workflows with realistic parameters | Check: do examples show the full flow (connect → call tools → format → deliver)? |

### Scoring Guide (applies to all 5 types)

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Workflow is complete for its type. All type-specific criteria met. Examples work. |
| 70-89 | Workflow is complete but some type-specific criteria lack detail. |
| 50-69 | Workflow has gaps relative to its type's requirements. |
| 30-49 | Incomplete workflow. Claude would need to improvise major steps. |
| 0-29 | No coherent workflow. Just a description of what the skill should do, not how. |

---

## Dimension 5: Error Handling (Weight: 10%)

Evaluates how the skill handles **failures, edge cases, and unexpected inputs**.

### Scoring Criteria

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-25 | **Fallback paths defined** — what to do when primary approach fails | Look for fallback/recovery sections or conditional logic |
| 0-25 | **Common failure cases covered** — at minimum: no results, invalid input, tool not available | Count addressed failure cases |
| 0-25 | **Graceful degradation** — skill provides partial value even when full execution fails | Check: does the skill have a degraded mode or helpful error message? |
| 0-25 | **No silent failures** — errors are surfaced to user, not swallowed | Check: does every error path end with user-facing communication? |

### Scoring Guide

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Comprehensive fallback for every failure mode. Graceful degradation. Honest error reporting. |
| 70-89 | Main failure cases covered. Some edge cases missing. |
| 50-69 | Only 1-2 failure cases addressed. Others would leave Claude stuck. |
| 30-49 | Minimal error handling. Claude would likely hallucinate on failure. |
| 0-29 | No error handling at all. |

---

## Dimension 6: Context Efficiency (Weight: 10%)

Evaluates how well the skill **manages the context window budget**.

### Scoring Criteria

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-25 | **No unnecessary information** — every line in SKILL.md earns its place | Ask for each section: "Would Claude make a mistake without this?" |
| 0-25 | **No information Claude already knows** — doesn't re-explain common knowledge | Check for explanations of widely-known concepts |
| 0-25 | **Heavy content is in references, not SKILL.md** — domain knowledge, large examples, lookup tables are deferred | Check: is SKILL.md bloated with data that should be in references? |
| 0-25 | **Metadata is compact** — name + description together stay under ~150 tokens | Estimate token count of frontmatter |

### Scoring Guide

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Every token is necessary. Perfect progressive disclosure. SKILL.md is lean. |
| 70-89 | Mostly efficient with minor bloat (a paragraph or two that could be cut). |
| 50-69 | Notable redundancy or unnecessary explanations. Could lose 30%+ without harm. |
| 30-49 | Significant bloat. Large knowledge sections in SKILL.md that should be deferred. |
| 0-29 | Massive context waste. Walls of text that Claude doesn't need. |

---

## Dimension 7: Portability & Compatibility (Weight: 10%)

Evaluates whether the skill **works across environments and is self-contained**.

### Scoring Criteria

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-25 | **Self-contained** — no external path references (../../shared/), all needed files are in the skill folder | Search for relative paths pointing outside the skill directory |
| 0-25 | **Cross-platform** — works on Claude Code, Claude.ai, and other SKILL.md-compatible agents, or explicitly states compatibility | Check compatibility field and instructions for environment-specific code |
| 0-25 | **Dependencies declared** — required CLIs, packages, APIs are listed with install instructions | Check for Prerequisites section or equivalent |
| 0-25 | **Environment check** — skill verifies its dependencies are available before proceeding | Check for Step 0 / environment verification logic |

### Scoring Guide

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Fully self-contained. Works everywhere. Dependencies declared and checked. |
| 70-89 | Mostly portable. Minor assumptions about environment. |
| 50-69 | Works in one environment but would fail in others. Missing dependency declarations. |
| 30-49 | References external paths. No dependency management. |
| 0-29 | Cannot function outside its original context. |

---

## Dimension 8: Safety & Robustness (Weight: 10%)

Evaluates the skill's **resilience against misuse and hallucination**.

### Scoring Criteria

| Points | Criterion | How to Check |
|--------|-----------|-------------|
| 0-25 | **Identity lock** (if applicable) — skill prevents Claude from substituting training data for real-time data | Check for "CRITICAL EXECUTION RULES" or equivalent guardrails |
| 0-25 | **No hallucination traps** — skill doesn't include large knowledge sections that Claude might use instead of executing commands | Check: does knowledge section have a "does NOT replace execution" disclaimer? |
| 0-25 | **No prompt injection risk** — skill doesn't contain patterns that could be exploited | Check for: raw user input passed unsanitized, eval() patterns, instructions to ignore previous context |
| 0-25 | **No harmful content** — skill doesn't facilitate unauthorized access, data exfiltration, or malicious behavior | Content safety review |

### Scoring Guide

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Strong guardrails. No hallucination traps. Safe content. Identity lock where appropriate. |
| 70-89 | Adequate safety. Minor risks (e.g., large knowledge section without disclaimer). |
| 50-69 | Some safety concerns. Missing guardrails for a CLI-wrapping skill. |
| 30-49 | Notable risks. Knowledge could easily override execution. |
| 0-29 | Active safety issues. Prompt injection vectors or harmful content. |

---

## Final Score Calculation

```
Final Score = Σ (dimension_score × dimension_weight)

Grade scale:
  A+ : 95-100  — Production-ready, exemplary skill
  A  : 90-94   — Excellent, minor polish needed
  B+ : 85-89   — Very good, a few improvements would help
  B  : 80-84   — Good, some issues to address
  C+ : 70-79   — Acceptable, needs work in several areas
  C  : 60-69   — Below average, significant improvements needed
  D  : 40-59   — Poor, fundamental issues
  F  : 0-39    — Nonfunctional or critically flawed
```
