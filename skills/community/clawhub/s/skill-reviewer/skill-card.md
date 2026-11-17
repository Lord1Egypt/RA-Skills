## Description:

Review and audit agent skills (SKILL.md files) for quality, correctness, and effectiveness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers, maintainers, and registry reviewers use this skill to evaluate agent skills before publishing, installing, comparing, or improving them. It provides structured review steps, scoring rubrics, defect checklists, and concise review templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review steps may encourage running untrusted or mutable remote commands from unknown skills.

Mitigation: Treat commands as review targets first; pin and verify installers before execution.

Risk: Testing copied commands on a normal workstation can expose local secrets or credentials.

Mitigation: Test untrusted skill commands only in a disposable sandbox without secrets, host mounts, credential agents, or broad network access.

## Reference(s):

- [Skill Reviewer release page](https://clawhub.ai/gitgoodordietrying/skills/skill-reviewer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with checklists, scorecards, defect lists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scoring rubrics and review verdicts for agent skill quality assessments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
