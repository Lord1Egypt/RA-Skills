# P03 Delegation handoff (incumbent brief)

## Objective

Produce a **handoff package** so the selected skill (incumbent) executes without redundant HR chatter and reports back in a shape you can log.

## Inputs

- `jd`: P01 JSON.
- `selected_skill`: `skill_id`, `name`, `description`, optional `references` hints.
- `user_verbatim`: key user quotes.
- `incident_stub`: proposed `incident_id` or filename stem.

## Procedure

1. Write **`context_for_incumbent`**: mission, success criteria, deliverables, constraints—no internal HR scoring prose.
2. Add **`do_not_do`**: scope cuts, forbidden actions (from user or policy).
3. Specify **`report_back_format`**: exact fields the incumbent should return after work (see below).
4. If the skill has a **canonical first step** visible in its SKILL.md opening, mention it once (do not paste entire SKILL.md).

## Output schema (JSON or Markdown sections)

```json
{
  "context_for_incumbent": "string",
  "do_not_do": ["string"],
  "report_back_format": {
    "summary": "1-3 sentences",
    "artifacts": ["paths or descriptions"],
    "success_against_criteria": [
      { "criterion": "string", "met": true, "notes": "string" }
    ],
    "blockers": ["string"],
    "follow_ups": ["string"]
  },
  "handoff_message_template": "string"
}
```

`handoff_message_template` should be copy-pasteable, e.g.:

> You are the incumbent for this task. Follow your SKILL.md. Context: … Success criteria: … Report back using the JSON shape in `report_back_format`.

## Quality gates

- Handoff must fit **under ~800 words** unless user supplied large specs (then point to paths).
- **Never** instruct the incumbent to edit `.skill-hr/registry.json` unless the task is HR meta-work.

## Failure modes

- **Leaky scoring** — Do not include numeric match scores in the handoff unless user asked for transparency.
- **Ambiguous owner** — If two skills co-own parts, split into two incidents or clarify sequential ownership.
