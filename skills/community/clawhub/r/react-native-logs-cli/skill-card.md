## Description:

Use rn-logs to read React Native Metro logs via CDP with plain-text output suitable for non-interactive agent runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okwasniewski](https://clawhub.ai/user/okwasniewski)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to install and run rn-logs for live or snapshot React Native Metro logs from a running app. It is suited for low-context troubleshooting where plain-text CLI output is preferable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global installation of rn-logs-cli can expose users to package supply-chain changes.

Mitigation: Install only from a trusted package source, prefer pinning a known version or using a project-local install, and avoid elevated privileges unless necessary.

Risk: The CLI cannot read useful logs unless Metro and the target React Native app are already running and reachable.

Mitigation: Confirm Metro host and port settings, ensure the app is running on a simulator or device, and specify --app when multiple apps are connected.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and plain-text CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Metro and a simulator or device with a running React Native app; pass --app when multiple apps are connected.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
