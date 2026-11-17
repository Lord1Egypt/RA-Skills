## Description:

Monitors local llama.cpp servers on macOS, auto-restarts on failure, sends notifications, and supports customizable hooks for self-healing supervision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gutchapa](https://clawhub.ai/user/gutchapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running local llama.cpp inference servers with OpenClaw use this skill to supervise health, restart failed services, align local configuration, and receive operational alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog can run indefinitely and perform automatic side effects, including rewriting local Pi configuration, restarting or force-killing llama-server processes, kickstarting an OpenClaw service, and sending Telegram alerts when credentials are present.

Mitigation: Review and harden the script before installation, run it as an unprivileged user, and start with DRY_RUN or notifications disabled until the operational effects are understood.

Risk: Evidence security guidance flags insecure command construction and process matching that should be reviewed before use.

Mitigation: Audit Python and AppleScript interpolation, constrain user-controlled environment values, and verify process matching targets only the intended local services.

## Reference(s):

- [Source repository](https://github.com/gutchapa/rock-solid-watchdog)
- [ClawHub skill page](https://clawhub.ai/gutchapa/skills/rock-solid-watchdog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
