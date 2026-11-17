## Description:

Captures learnings, errors, feature requests, and corrections in project learning files so coding agents can improve future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marveldcdad-eng](https://clawhub.ai/user/marveldcdad-eng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to log command failures, user corrections, missing capabilities, API issues, and reusable best practices. The logged entries can later be reviewed, resolved, or promoted into project memory and agent instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived logs may persist secrets, credentials, customer data, private transcripts, or other sensitive context.

Mitigation: Redact sensitive data before writing learning entries and avoid logging raw request bodies or private transcripts.

Risk: Promoting learnings into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions can affect future agent behavior too broadly.

Mitigation: Require human review before updating persistent instruction files and promote only concise, broadly applicable guidance.

Risk: Optional hooks can add broad automatic reminders or error-detection behavior across sessions.

Mitigation: Keep hooks disabled unless the user explicitly wants automatic reminders and has reviewed the hook behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marveldcdad-eng/skills/self-improving-agent-4)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands, markdown templates, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent learning files and agent instruction files when the user or workflow chooses to apply the guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
