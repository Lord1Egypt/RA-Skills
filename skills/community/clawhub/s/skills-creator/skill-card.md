## Description:

Guide users through creating, reviewing, and improving OpenClaw skills following proven best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jau123](https://clawhub.ai/user/jau123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create, review, retrofit, and publish OpenClaw or ClawHub skills with stronger triggering, structure, metadata, and security review habits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated wording may make security-relevant behavior less transparent to reviewers.

Mitigation: Review generated security language against the actual uploads, public links, API calls, and execution behavior before publication.

Risk: Generated API wrapper scripts may handle API keys, paid services, or external requests incorrectly if used without review.

Mitigation: Require human code review, declare required environment variables and binaries, pin package versions, and test scripts before use.

Risk: Generated shell commands or scripts could be executed before the user has confirmed they are appropriate.

Mitigation: Present generated scripts and commands for user approval and avoid running newly created scripts without explicit confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jau123/skills/skills-creator)
- [Best Practices for OpenClaw Skills](references/best-practices.md)
- [Quality Checklist](references/quality-checklist.md)
- [Skill Template](assets/skill-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables, checklists, code blocks, and generated skill file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts and security wording require human review before execution or publication.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
