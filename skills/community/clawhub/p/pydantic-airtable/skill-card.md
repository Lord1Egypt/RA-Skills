## Description:

Manage Airtable tables and records via the pydantic-airtable Python library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grishick](https://clawhub.ai/user/grishick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Airtable bases, tables, schemas, and records through pydantic-airtable scripts or reusable Python snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can create, update, or delete Airtable records and tables when valid credentials are present.

Mitigation: Use a token scoped to the specific base and permissions needed, test against a non-production base first, and double-check record or table IDs before destructive operations.

Risk: Model-driven operations import and execute the referenced local Python module.

Mitigation: Run model operations only with trusted local code, preferably inside an isolated virtualenv or container.

Risk: The bundled scripts can read JSON payloads from local @file.json arguments.

Mitigation: Inspect JSON files before passing them to record or table commands.

## Reference(s):

- [pydantic-airtable API surface](artifact/references/api-surface.md)
- [Airtable w/Python on ClawHub](https://clawhub.ai/grishick/skills/pydantic-airtable)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that call Airtable APIs using AIRTABLE_ACCESS_TOKEN and AIRTABLE_BASE_ID.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
