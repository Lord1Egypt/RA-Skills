## Description:

Session Manager helps an agent detect topic changes, ask whether to start a new session, and save user-selected session records to Feishu Bitable or local Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zh40](https://clawhub.ai/user/zh40)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to organize ongoing work into explicit sessions, preserve selected context across topic changes, and record summaries, decisions, and follow-up tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session records may contain sensitive conversation metadata, summaries, decisions, or follow-up tasks.

Mitigation: Choose a storage location with appropriate access controls, prefer local Markdown when more control is needed, and avoid saving highly sensitive sessions unless retention and deletion practices are clear.

Risk: Feishu Bitable storage can expose session records to workspace permissions outside the agent's control.

Mitigation: Use a preconfigured Bitable only after confirming who can access it, or select local Markdown storage for tighter control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zh40/skills/session-manager)
- [Session template](references/session-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown session records, Feishu Bitable field guidance, and concise user prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update user-selected session records and MEMORY.md state when the user has chosen a storage mode.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
