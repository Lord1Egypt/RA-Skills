## Description:

Track skill versions, benchmark performance, compare improvements, and get self-improvement signals. Integrates with tasktime and ClawVault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and agent operators use SkillBench to record skill benchmark results, compare skill versions, run benchmark checks, export reports, and identify improvement signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned global npm CLI package.

Mitigation: Use a pinned package version and inspect the CLI source or package provenance before installing.

Risk: Benchmark metadata may sync to ClawVault, including sensitive task names or error details.

Mitigation: Confirm sync behavior can be disabled or reviewed before recording sensitive benchmark data.

## Reference(s):

- [SkillBench ClawHub page](https://clawhub.ai/g9pedro/skills/skillbench)
- [Publisher profile](https://clawhub.ai/user/g9pedro)
- [ClawVault](https://clawvault.dev)
- [tasktime](https://clawhub.com/skills/tasktime)
- [ClawHub](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe JSON, Markdown, dashboard, badge, CI, and cron outputs produced by the SkillBench CLI.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
