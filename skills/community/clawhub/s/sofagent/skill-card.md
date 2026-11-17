## Description:

FDE Skill guides agents through enterprise AI discovery, assessment, delivery, and follow-up, with practices for constraining agent behavior, auditing changes, and retaining lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongfangxun](https://clawhub.ai/user/kongfangxun)

### License/Terms of Use:

MIT-0

## Use Case:

Front-line deployment engineers and developers use it to assess enterprise AI workflows, identify and quantify suitable AI tasks, and guide delivery and follow-up of tailored skills and governance practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible external model data sharing.

Mitigation: Review the data-sharing path and destinations before installation; avoid sending sensitive data unless the path is approved.

Risk: The security review flags an unpinned package execution path.

Mitigation: Review installation behavior and package sources before installing, and use a controlled environment.

Risk: Some testing guidance could touch operational knowledge data.

Mitigation: Review test steps first and use non-production or sanitized knowledge data where practical.

Risk: The scan was incomplete because a referenced path was missing.

Mitigation: Resolve the missing path and repeat the review before treating the scan as comprehensive.

## Reference(s):

- [FDE Skill on ClawHub](https://clawhub.ai/kongfangxun/skills/sofagent)
- [SKILL.state execution protocol paper](https://arxiv.org/abs/2608.26263)
- [DeepAgentsJS](https://github.com/langchain-ai/deepagentsjs)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Markdown with tables, checklists, audit summaries, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-specific structured guidance; no fixed output schema.]

## Skill Version(s):

1.9.0 (source: artifact/SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
