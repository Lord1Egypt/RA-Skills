## Description:

Use when an agent should answer simple operations questions by retrieving internal wiki content through wiki MCP, and must refuse to answer when the wiki does not provide enough evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glylovechina](https://clawhub.ai/user/glylovechina)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to answer document-oriented operations questions from internal wiki pages for deployment, release, rollback, restart, logs, alerts, SOPs, permissions, and configuration details. It refuses or answers conservatively when retrieved wiki evidence is missing, incomplete, or conflicting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may retrieve and summarize internal operations documentation.

Mitigation: Install only where read-only internal wiki access is appropriate.

Risk: Weak or missing wiki evidence could lead to unsupported operational steps.

Mitigation: Use the skill's evidence-only response contract and refuse or answer conservatively when wiki results are missing, incomplete, or conflicting.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown responses with wiki evidence summaries and refusal statements when evidence is insufficient]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are constrained to retrieved wiki MCP content and should separate direct conclusions, supporting evidence, and unknowns.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
