## Description:

Real-time companion monitor for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luccast](https://clawhub.ai/user/luccast)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, verify, and run Crabwalk as a real-time monitor for OpenClaw agent activity, then share a reachable monitor URL with a human collaborator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and runs a remote release artifact from the publisher's GitHub release pipeline.

Mitigation: Install only after trusting the publisher and prefer a pinned, verified release.

Risk: The install flow may modify shell startup files and use sudo to install optional qrencode support.

Mitigation: Review shell profile changes before accepting them and avoid allowing optional sudo package installation unless needed.

Risk: The monitor can expose agent activity and workspace browsing over a network-accessible service.

Mitigation: Bind to localhost unless authenticated network access is required and acceptable.

## Reference(s):

- [Crabwalk homepage](https://crabwalk.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, verification, startup, update, and CLI usage guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
