## Description: <br>
Run and script the XMTP CLI for testing, debugging, and interacting with XMTP conversations, groups, messages, setup, permissions, syncing, and content examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humanagent](https://clawhub.ai/user/humanagent) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, and operate the XMTP CLI for testing, debugging, sending messages, listing conversations, syncing, managing groups, and changing permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: XMTP CLI setup uses wallet and database encryption keys that can expose accounts or local message data if shared. <br>
Mitigation: Use dev or ephemeral keys for testing, keep .env files out of git and logs, and restrict access to wallet and database keys. <br>
Risk: Commands can send messages, create groups, or change group permissions for real recipients. <br>
Mitigation: Double-check target addresses, group IDs, member lists, and permission changes before running commands. <br>


## Reference(s): <br>
- [XMTP documentation](https://docs.xmtp.org) <br>
- [XMTP debug agents documentation](https://docs.xmtp.org/agents/debug-agents) <br>
- [ClawHub skill page](https://clawhub.ai/humanagent/xmtp-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that send messages, create groups, update permissions, or read local XMTP CLI configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
