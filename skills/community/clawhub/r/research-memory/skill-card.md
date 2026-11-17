## Description:

Give AI agents persistent BlueColumn research memory for storing, recalling, and searching research findings; requires a BlueColumn API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when an agent needs to preserve research summaries across interactions, recall prior findings, or add quick notes to BlueColumn persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research summaries may be sent to and persisted in BlueColumn/Supabase remote storage.

Mitigation: Store or recall only research that is approved for external persistence, and avoid secrets, credentials, confidential data, or regulated personal information.

Risk: The skill can encourage memory operations without enough explicit consent or scoping.

Mitigation: Require explicit user approval before each store or recall operation and use a dedicated BlueColumn API key with the narrowest practical access.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub research-memory skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/research-memory)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or retrieve research summaries through BlueColumn remote persistent storage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
