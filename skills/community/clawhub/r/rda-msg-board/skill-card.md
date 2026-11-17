## Description:

Send scrolling text messages to RDA MSG Board via HTTP/JSON for notifications, alerts, or status updates on a physical LED matrix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rdeangel](https://clawhub.ai/user/rdeangel)

### License/Terms of Use:


## Use Case:

Developers, operators, and automation agents use this skill to send status messages, alerts, and notifications to configured RDA MSG Board LED matrix devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Board credentials may be stored in boards.yaml or environment variables.

Mitigation: Treat boards.yaml as a secret file, avoid default or reused passwords, and limit access to configured environments.

Risk: Messages may be sent over plain HTTP to a physical device on the network.

Mitigation: Use the skill only with trusted boards on trusted networks, and prefer HTTPS or an isolated management network where possible.

Risk: Ambiguous user requests could send unintended content to a visible display.

Mitigation: Require explicit user confirmation for ambiguous send requests, especially alerts or public-facing messages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rdeangel/skills/rda-msg-board)
- [Publisher Profile](https://clawhub.ai/user/rdeangel)
- [RDA MSG Board Project](https://github.com/rdeangel/rda_msg_board)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Python scripts that send HTTP JSON requests to configured message board devices.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
