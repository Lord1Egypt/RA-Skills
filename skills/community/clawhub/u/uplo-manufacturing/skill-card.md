## Description:

AI-powered manufacturing knowledge management. Search work orders, quality inspections, production schedules, and equipment maintenance records with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing teams use this skill to search and connect plant-floor knowledge such as work orders, inspection records, production schedules, CAPA records, maintenance logs, equipment manuals, and revision-controlled procedures. It supports root cause analysis, preventive maintenance planning, material traceability, document updates, and escalation to knowledge owners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned MCP package with an API key.

Mitigation: Install only from a trusted UPLO MCP package source, prefer a pinned MCP package version, and provide a narrowly scoped UPLO token.

Risk: The skill can retrieve broad organizational context, including full organizational export and session-start identity or status context.

Mitigation: Confirm that broad context retrieval is acceptable for the environment and rely on server-side authorization, auditing, and data-minimization controls.

Risk: Manufacturing answers can affect quality, maintenance, revision control, and safety-sensitive decisions.

Mitigation: Review retrieved records before acting, check document revision levels, and escalate recurring quality failures or overdue maintenance to the responsible owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-manufacturing)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool-call examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a UPLO instance URL and API key; MCP responses may include work orders, quality records, maintenance history, organizational context, directives, and knowledge-owner information.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
