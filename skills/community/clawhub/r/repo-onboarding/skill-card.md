## Description:

Onboard a coding repository with both technical architecture intake and execution governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill when starting work in a new or existing repository to capture architecture, dependency, run, build, and test context, then establish roadmap and kanban execution artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run unreviewed local scripts from absolute paths.

Mitigation: Review the exact local files before execution, confirm the repository changes they will make, and prefer package-relative reviewed scripts.

Risk: The optional daily PM audit installs a persistent cron task.

Mitigation: Enable the cron task only with explicit user approval, document how to remove it, and confirm the schedule, timezone, and agent command before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/broedkrummen/skills/repo-onboarding)
- [Repo Onboarding Report template](references/onboarding-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated repository documentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces architecture, dependency, roadmap, kanban, and onboarding-report artifacts when the referenced workflows complete.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
