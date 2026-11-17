## Description:

Diagnoses WebSocket connection latency by measuring DNS lookup, TCP handshake, TLS handshake, and WebSocket Upgrade timing for ws and wss endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jizhouli](https://clawhub.ai/user/jizhouli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run shell-based WebSocket latency checks, compare ws and wss connection behavior, and troubleshoot slow connection stages for authorized endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and diagnostic scripts can perform high-impact shell and network actions.

Mitigation: Audit the shell scripts before use, avoid running the sudo installer blindly, and install dependencies manually where practical.

Risk: WebSocket checks can send network traffic to sensitive or unauthorized targets.

Mitigation: Run diagnostics only against endpoints you own or are explicitly authorized to test, and avoid private or internal targets unless intentional.

Risk: Unvalidated test rounds can increase repeated network activity.

Mitigation: Validate the rounds argument as a simple integer from 1 to 10 before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jizhouli/skills/tencentcloud-websocket-checker)
- [README](docs/README.md)
- [Examples](docs/EXAMPLES.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Reference examples](references/examples.md)
- [Reference troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance with optional CSV or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network diagnostics depend on bash, curl, dig, awk, sed, and authorized target endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
