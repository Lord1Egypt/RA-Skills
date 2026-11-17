## Description:

BotLearn Healthcheck is an autonomous OpenClaw health inspector that checks hardware, configuration, security, skills, and autonomy signals, then produces diagnostic reports and fix guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect a live OpenClaw instance, summarize health across core operating domains, and generate actionable diagnostic reports. It is intended for troubleshooting, system status checks, and guided remediation after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive OpenClaw configuration, logs, identity and workspace files, and security data.

Mitigation: Review the skill before installation, run it only in environments where that access is acceptable, and prefer narrower collection with explicit consent before diagnostics.

Risk: The skill writes persistent local health reports that may contain diagnostic details from the inspected instance.

Mitigation: Define where reports are retained, who can access them, and when they should be deleted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/xiaoding-botlearn-healthcheck)
- [Publisher profile](https://clawhub.ai/user/asterisk622)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports and concise diagnostic guidance, with optional HTML report files and shell commands for checks or fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under the OpenClaw health-reports memory path when the skill runs.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter version is 0.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
