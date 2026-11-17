## Description:

WSL2 HTTP proxy setup via Windows host. Automatically detects proxy running on Windows (Clash/V2Ray/SS/Surge etc.) and configures WSL2 environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ham-5on](https://clawhub.ai/user/ham-5on)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers working in WSL2 use this skill to detect a Windows-hosted HTTP proxy, set shell proxy environment variables, verify outbound connectivity, and clear proxy settings when they are no longer needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans common proxy ports on the WSL2 gateway.

Mitigation: Run it only in WSL2 environments where discovering a Windows-hosted local proxy is expected.

Risk: Proxy environment variables can route future shell commands through the detected proxy.

Mitigation: Apply the exported variables only for the intended session, avoid adding them to shell startup files unless persistent routing is desired, and use unset_proxy.sh to clear them.

Risk: Status checks may print proxy host, port, and environment variable values.

Mitigation: Review command output before sharing logs or terminal transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ham-5on/skills/wsl-proxy)
- [Publisher profile](https://clawhub.ai/user/ham-5on)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and shell output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit environment variable exports for the current shell when setup_proxy.sh is evaluated.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
