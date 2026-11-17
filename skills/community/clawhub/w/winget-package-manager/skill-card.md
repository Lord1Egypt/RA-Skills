## Description:

Controlled Windows package management workflow based on winget that guides an agent to safely search, inspect, download, install, upgrade, uninstall, and list upgradeable applications on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiapeng](https://clawhub.ai/user/hongjiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and Windows users use this skill to have an agent manage applications through WinGet while applying package identity checks, approved source limits, and disambiguation before medium- or high-risk actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install, upgrade, download, and uninstall requests can modify the local Windows system or retrieve installer packages.

Mitigation: Review these requests before execution, prefer exact package IDs, and limit actions to approved WinGet sources.

Risk: Ambiguous package names can cause the agent to act on the wrong application.

Mitigation: Require package search or inspection and ask the user to choose when multiple candidates match.

Risk: Uninstall operations are high-risk and may report success even when the application remains installed.

Mitigation: Use exact package IDs, avoid automatic retries, and perform a post-check when the host allows it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiapeng/skills/winget-package-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/hongjiapeng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command examples and JSON-like structured results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only workflow; command execution depends on a Windows host with winget available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
