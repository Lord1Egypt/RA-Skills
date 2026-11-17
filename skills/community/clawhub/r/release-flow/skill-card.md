## Description:

Release Flow is a project-specific Git workflow coordinator for redfoxhub-html that helps agents start feature branches, deploy changes to the test branch, and promote verified work to production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xue-xiao-yu](https://clawhub.ai/user/xue-xiao-yu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to keep redfoxhub-html feature, test, and production Git flows consistent. It guides branch naming, branch synchronization, merges, pushes, production confirmation, and conflict handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push to develop and master, including production release triggers.

Mitigation: Install it only for the intended redfoxhub-html repository, review the printed command list before any push or production release, and prefer protected branches or Merge Requests where available.

Risk: Branch and user values may be used in Bash commands without clear safety validation.

Mitigation: Confirm branch names contain only simple safe characters before running push or release commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xue-xiao-yu/skills/release-flow)
- [redfoxhub-html test pipeline](https://flow.aliyun.com/pipelines/4962314/current)
- [redfoxhub-html production pipeline](https://flow.aliyun.com/pipelines/4946808/current)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command blocks and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
