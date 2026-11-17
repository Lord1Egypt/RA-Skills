## Description:

RevSec Shield monitors an OpenClaw agent for prompt injection, malicious skills, configuration changes, and data exfiltration indicators, then sends plain-English alerts through WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[revupai](https://clawhub.ai/user/revupai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to install continuous security monitoring, register agent metadata with RevSec, poll for alerts, and request manual protection summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently creates and repairs a persistent five-minute OpenClaw background task.

Mitigation: Review the scheduled cron job before installation and confirm how to disable the job and remove local state if monitoring is turned off.

Risk: The skill makes recurring outbound calls to RevSec and shares identifying agent metadata such as hostname, model, and installed-skill names.

Mitigation: Use the skill only when that metadata sharing is acceptable for the agent environment and account policy.

Risk: The setup flow may expose the REVSEC_API_KEY if it prints the environment variable while checking configuration.

Mitigation: Check or edit the setup flow so the API key presence is verified without echoing the secret value.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/revupai/skills/revsec-shield)
- [RevSec homepage](https://revsec.revt2d.com)
- [RevSec dashboard](https://revsec.revt2d.com/personal)
- [RevSec signup](https://revsec.revt2d.com/signup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local state and a recurring OpenClaw cron job during setup.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
