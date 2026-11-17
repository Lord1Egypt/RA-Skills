## Description:

QClaw Self-Evolver helps agents maintain local learning records, assess skill health, run SEA self-evolution scans, and generate candidate skills from recurring workflow patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qshan1](https://clawhub.ai/user/qshan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install a self-evolution workflow that records corrections, reviews skill metrics, runs periodic SEA scans, and drafts candidate skills from repeated tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local learning records, corrections, and error logs may capture sensitive information.

Mitigation: Avoid storing secrets in corrections or logs, and review learning files before sharing or enabling generated skills.

Risk: The installation flow can register recurring background agent activity.

Mitigation: Disable or remove the SEA-Evolution-Scan cron job unless recurring self-evolution scans are explicitly desired.

Risk: Generated candidate skills or instruction changes may be based on stored corrections without strong approval boundaries.

Mitigation: Review and scan generated skills and proposed instruction changes before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qshan1/skills/qclaw-self-evolver)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown records and reports, JSON status data, generated SKILL.md files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local learning records, skill metrics, workspace scripts, generated skill directories, and a recurring SEA-Evolution-Scan cron job.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
