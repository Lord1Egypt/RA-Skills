## Description:

Manage tasks, columns, and documents on the Rectify platform via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umar-lateef](https://clawhub.ai/user/umar-lateef)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to let agents manage Rectify AgentPulse task boards and Rectify Documents, including creating, updating, moving, searching, archiving, and deleting project records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Rectify project token can read and modify project tasks and documents.

Mitigation: Install the skill only for trusted agents and use a token scoped to the intended workspace or project when available.

Risk: Task, column, and document operations include archive, delete, and permanent deletion paths.

Mitigation: Review destructive requests carefully, especially column deletion and permanent document deletion, before allowing the agent to proceed.

## Reference(s):

- [Rectify product site](https://www.rectify.so)
- [ClawHub Rectify skill page](https://clawhub.ai/umar-lateef/skills/rectify-skill)
- [Publisher profile](https://clawhub.ai/user/umar-lateef)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses RECTIFY_PROJECT_TOKEN to call Rectify REST endpoints and returns concise action confirmations or API error details.]

## Skill Version(s):

1.0.2 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
