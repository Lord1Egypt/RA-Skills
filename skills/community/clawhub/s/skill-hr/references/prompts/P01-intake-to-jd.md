# P01 Intake → Job Description (JD)

## Objective

Turn a vague user request into a structured **Job Description** so skills can be matched or recruited without ambiguity.

## Inputs

- `user_task`: raw user message and follow-ups.
- `workspace_hints`: repo type, languages, constraints mentioned.
- `registry_summary`: optional list of `id`, `name`, `status` from `.skill-hr/registry.json`.

## Procedure

1. Restate the **outcome** in one sentence (what "done" looks like).
2. Extract **must-have competencies** (capabilities, not tool names, unless the user insisted).
3. Extract **nice-to-have** items.
4. List **tools_and_access** (APIs, CLIs, browsers, files) the incumbent likely needs.
5. Define **deliverables** (artifacts, formats).
6. Capture **constraints** (time, privacy, offline, "no new deps", etc.).
7. Write **success_criteria** as checkable bullets.
8. Note **risk_notes** (ambiguity, missing credentials, legal/safety).
9. Assign **complexity_tier**: `S` (single file / one-shot), `M` (multi-step same domain), `L` (cross-domain or high uncertainty).
10. **Retrieval helpers (for P02a)** — always emit:
    - `search_queries`: **3–5** short strings a search tool could run against skill names/descriptions/bodies (synonyms, artifact types, integrations).
    - `competency_tags`: **3–8** tokens from [`../01-competency-model.md`](../01-competency-model.md) dimensions (e.g. `artifact_mastery:pdf`, `integration:mcp`, `workflow_depth:L2`).

## Output schema (JSON)

```json
{
  "role_title": "string",
  "mission_statement": "string",
  "must_have_competencies": ["string"],
  "nice_to_have": ["string"],
  "tools_and_access": ["string"],
  "deliverables": ["string"],
  "constraints": ["string"],
  "success_criteria": ["string"],
  "risk_notes": ["string"],
  "complexity_tier": "S|M|L",
  "search_queries": ["string"],
  "competency_tags": ["string"]
}
```

## Quality gates

- Every `must_have_competencies` item must be **testable** or **observable** in the final output.
- If the user goal is contradictory, **stop** and ask one clarifying question before finalizing JD.

## Failure modes

- **Overfitting to tools** — User said "use X"; still capture the underlying competency (e.g. "static analysis" not only "eslint").
- **Scope creep** — Split into primary JD + "stretch" section in `nice_to_have`.
