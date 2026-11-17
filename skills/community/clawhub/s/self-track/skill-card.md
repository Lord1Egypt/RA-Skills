## Description:

Self-Track is Sig Botti's self-improvement tracking system for logging learning, capability gaps, weekly reviews, and skill-building progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louch84](https://clawhub.ai/user/louch84)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Self-Track to help an agent maintain a personal learning loop: record capability gaps, log lessons, review progress, and outline skill-building steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad self-tracking triggers may cause persistent memory writes or vector-memory additions without enough user review.

Mitigation: Require explicit confirmation before writing memory files, adding vector-memory entries, or updating long-term memory.

Risk: Skill-building steps may create, validate, commit, or push new skills.

Mitigation: Require review and approval before creating new skills, committing changes, or pushing to remotes.

Risk: Learning records may capture sensitive personal, project, or operational information.

Mitigation: Limit logged content to non-sensitive information and review records before sharing or publishing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and file-update instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct persistent memory/file updates and vector-memory additions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
