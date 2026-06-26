# Correctness Findings

**Target:** /Users/akkari/.openclaw/public/repos/sharedintellect-quorum/ports/claude-code/SKILL.md
**Rubric:** Agent Configuration Rubric
**Critic:** Correctness
**Timestamp:** 2026-03-12 Pacific

---

### AC-002: Agent permissions are scoped to minimum required capabilities
- **Verdict:** FAIL
- **Severity:** HIGH
- **Evidence:** "For each critic, use the Agent tool with these parameters: - `run_in_background: true` — all 4 critics run in parallel - `model: "sonnet"` — critics run on Sonnet (Tier 2)." (Section: 4. Critic Dispatch (Parallel))
- **Explanation:** The critic dispatch instructions specify `run_in_background` and `model` parameters for the Agent tool, but do not specify any permission scoping or capability restrictions for the delegated agents. Each critic sub-agent inherits the full tool suite of the orchestrator (Read, Write, Bash, Edit, Grep, Glob, Agent, etc.) despite only needing Read access to evaluate artifacts. There is no `allowed_tools`, `permissions`, or equivalent constraint declared anywhere in the dispatch configuration. The pre-screen step also invokes `python3` via the Bash tool with no sandbox or filesystem restriction specified. Additional instances exist in Section 10 (cross-consistency critic dispatch) and Section 11 (single-critic mode dispatch), which similarly omit permission scoping.

### AC-006: API keys and secrets are referenced via environment variables, not hardcoded
- **Verdict:** PASS
- **Severity:** CRITICAL
- **Evidence:** No hardcoded API keys, secrets, bearer tokens, or credential patterns found anywhere in the artifact.
- **Explanation:** A thorough search for patterns matching `sk-`, `Bearer`, `token:`, `api_key`, `password`, and `secret` literal values returned zero matches. The artifact does not reference any API keys or credentials at all — authentication is implicitly handled by the Claude Code runtime environment.

### AC-008: Delegating agents specify acceptance criteria for their delegatees
- **Verdict:** PASS
- **Severity:** HIGH
- **Evidence:** "**Acceptance criteria for critic delegations:** A critic response is considered successful ONLY if ALL of the following are true: 1. The response is valid JSON matching FINDINGS_SCHEMA. 2. Every finding in the response has non-empty `evidence_tool` or `evidence_result` (per section 9). 3. The critic has addressed at least one rubric criterion..." (Section: 4. Critic Dispatch (Parallel))
- **Explanation:** The artifact explicitly defines acceptance criteria for critic delegations with three specific, verifiable conditions. The criteria are well-defined and include a fallback for empty responses: "A response of `{"findings": []}` is valid ONLY if it is accompanied by a brief confirmation that the critic evaluated the artifact and found no issues." This adequately specifies success conditions for delegated agents.

### AC-009: Configuration version is specified and matches schema version
- **Verdict:** FAIL
- **Severity:** LOW
- **Evidence:** The artifact contains no top-level version field. The only version references are: "Also extract the rubric metadata fields: `name`, `domain`, `version`." (Section: 2. Rubric Selection) and "## Rubric: {rubric_name} (v{rubric_version})" (Section: 5. Prompt Construction) — both refer to the rubric's version, not the SKILL.md configuration's own version.
- **Explanation:** The SKILL.md file functions as an agent configuration document but lacks its own version identifier. There is no version field at the top of the document, no schema version declaration, and no compatibility statement. This makes it impossible to track which version of the skill configuration is deployed or to validate it against a schema version. The version references present in the file (lines 41, 112) pertain to the rubric metadata being consumed, not to the skill configuration itself.

### unsanitized-prompt-interpolation [MANDATORY]
- **Verdict:** FAIL
- **Severity:** HIGH
- **Evidence:** "{artifact_text}" is interpolated directly into the critic prompt template within `<artifact>` tags (Section: 5. Prompt Construction for Each Critic), along with "{formatted_criteria_list}", "{formatted_prescreen_results}", "{artifact_a_text}", "{artifact_b_text}", "{prescreen_a_results}", and "{prescreen_b_results}" (Sections: 5 and 10).
- **Explanation:** The prompt construction template in Section 5 interpolates file-derived content (`artifact_text`, `formatted_prescreen_results`) and rubric-derived content (`formatted_criteria_list`) directly into the LLM prompt with no sanitization step. A malicious or adversarial artifact could contain text that mimics prompt structure (e.g., injecting a fake `## Your Task` section or a `Respond ONLY with` override) to manipulate critic behavior. There is no instruction to escape, sanitize, or validate the interpolated content before insertion. The `<artifact>` XML tags provide minimal structural delineation but are not a sanitization mechanism — they can be closed and reopened by adversarial content within the artifact text. Additional instances exist in Section 10 (cross-artifact mode) where two artifacts are interpolated.

### broad-except-no-traceback [MANDATORY]
- **Verdict:** NOT_APPLICABLE
- **Severity:** MANDATORY
- **Evidence:** N/A
- **Explanation:** This criterion targets Python `except Exception` blocks that discard traceback information. The SKILL.md artifact is a Markdown-based agent configuration document, not Python source code. It contains no `except` blocks, `try/except` constructs, or exception handling code. The error handling described in Section 12 is declarative (a table of failure modes and actions), not executable Python.

---

## Summary
- **PASS:** 2 | **FAIL:** 3 | **NOT_APPLICABLE:** 1
- **Most critical finding:** unsanitized-prompt-interpolation — File-derived artifact content is interpolated into LLM prompts via raw template substitution with no sanitization, enabling potential prompt injection by adversarial artifacts.
