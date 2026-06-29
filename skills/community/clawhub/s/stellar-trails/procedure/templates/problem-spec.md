# Problem Specification

This template is the output of the SPECIFY phase. Every field is required. Leaving a field empty indicates the analysis was incomplete — revisit before proceeding.

## Why This Template Exists

A specification forces precise thinking before code is written. Ambiguity in requirements is the most common source of rework. By filling out every field, the agent demonstrates understanding and the user can confirm or correct before any code changes occur.

---

## Template

Copy and complete the following for every task:

```markdown
# Problem Specification

| Field | Value |
|-------|-------|
| Request | [Exact user request — quoted verbatim] |
| Source Research | [Existing solutions found, official docs consulted, patterns identified. If none found, state explicitly.] |
| Functional Requirement | [What the code must accomplish — stated precisely] |
| Technical Constraints | [Platform limits, sandbox rules, framework requirements] |
| Identified Edge Cases | [List each edge case with handling strategy] |
| Affected Files | [See table below] |
| Risk Level | [LOW / MEDIUM / HIGH with justification] |
| Dependencies | [External packages, services, config changes needed] |
| Source State | [Branch name, HEAD commit SHA, and verification status. Example: "renuked @ 3283d1f (verified via git fetch, local matches remote)" or "No git repository involved"] |
| Scope OUT | [Explicitly excluded from this task — prevents scope creep. If nothing is excluded, write "None — task is fully scoped." Standard/Complex tasks should always have explicit exclusions.] |

## Affected Files

| File Path | Action | Purpose |
|-----------|--------|---------|
| path/to/file | Create / Modify | Why this file needs to change |
| path/to/file | Create / Modify | Why this file needs to change |

## Edge Cases

| # | Edge Case | Handling Strategy |
|---|-----------|-------------------|
| 1 | [Describe the edge condition] | [How the code will handle it] |
| 2 | [Describe the edge condition] | [How the code will handle it] |

## Notes

[Any additional context, assumptions, or clarifications]
```

---

## Field Guidance

| Field | Guidance |
|-------|----------|
| **Request** | Quote the user's exact words. Do not paraphrase. This anchors the specification to the original intent. |
| **Source Research** | Document what sources were checked: existing packages/libraries found, official docs read, known patterns identified. If no existing solution was found, state explicitly — e.g., "Searched npm for X, checked Next.js docs for Y — no existing package or built-in method found." Building from scratch when a library exists is a spec-level defect. |
| **Functional Requirement** | Translate the request into a precise technical statement. Use "must" language: "The system must render a list of items sorted by creation date." |
| **Technical Constraints** | Reference `knowledge/universal/architecture.md` for general constraints and `knowledge/platform/zai-sandbox.md` for sandbox-specific rules. Include framework requirements (e.g., "Must use server components for data fetching"). |
| **Identified Edge Cases** | Think about empty inputs, missing data, concurrent operations, boundary values, and error states. Each edge case needs a concrete handling strategy, not just identification. |
| **Affected Files** | Every file that will be created or modified must be listed. The action column uses "Create" for new files and "Modify" for existing files. |
| **Risk Level** | LOW = single file, well-understood pattern. MEDIUM = multiple files or minor uncertainty. HIGH = schema changes, architectural impact, or significant uncertainty. Justify the rating. |
| **Dependencies** | Include packages to install, services that must be running, and configuration changes. If none, write "None." |
| **Source State** | If the task involves a git repository, record the branch and HEAD SHA after running Source State Verification (see SKILL.md). This creates an immutable reference point for the analysis. If no git repository is involved, write "No git repository involved." |
| **Scope OUT** | REQUIRED for Standard/Complex tasks. Explicitly list what is NOT part of this task. This feeds the Scope's Scope OUT field and the delivery report's Scope Drift comparison. Prevents scope creep by making exclusions visible before implementation starts. |

---

## Complexity Tier Abbreviation

For simple tasks (single file, no schema change, no new dependencies), SPECIFY and PLAN may be combined into one output. The problem specification fields above are still required — they appear in the combined document alongside the implementation plan fields from `procedure/templates/implementation-plan.md`.
