## Description:

Auto Optimizer monitors OpenClaw skill performance, analyzes bottlenecks, generates optimization recommendations, and can apply code changes to improve efficiency and stability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to monitor OpenClaw skill performance, identify bottlenecks, and generate or apply optimization plans for skill code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change other skills' code and metric files.

Mitigation: Use it only in a version-controlled workspace, review generated plans, prefer dry-run or preview behavior where available, and inspect diffs before accepting changes.

Risk: Weak path scoping and missing explicit approval gates can make untrusted skill names or paths unsafe.

Mitigation: Pass only trusted, explicit skill paths; validate path scope before execution; and require human confirmation before applying optimizations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-auto-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JavaScript objects, Markdown reports, and proposed or applied code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write performance metrics, create backups, and modify target skill files when optimization application is used.]

## Skill Version(s):

0.1.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
