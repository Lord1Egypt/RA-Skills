## Description: <br>
Industrial-grade secure bridge to Bitwarden that copies passwords and TOTP codes with zero-trust kernel-level piping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chyern](https://clawhub.ai/user/chyern) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Bitwarden CLI users use this skill to let an agent search vault item metadata and copy selected passwords or TOTP codes to the native clipboard without printing the secret in agent output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can search Bitwarden item names and usernames. <br>
Mitigation: Use the skill only where exposing vault metadata to the agent is acceptable. <br>
Risk: Copied passwords or TOTP codes may remain in clipboard history or sync services. <br>
Mitigation: Disable clipboard history and clipboard sync for sensitive use, and clear the clipboard after use. <br>
Risk: BW_SESSION grants access to the unlocked Bitwarden vault. <br>
Mitigation: Protect BW_SESSION like a password and unset or expire it when the workflow is complete. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/chyern/safe-bitwarden-cli) <br>
- [Project homepage](https://github.com/chyern/Agent-Skills) <br>
- [Bitwarden CLI](https://github.com/bitwarden/clients/tree/master/apps/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON objects or arrays for setup and search results, plus plain text status messages for copy actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BW_SESSION and Bitwarden CLI; selected passwords and TOTP codes are copied to the native OS clipboard.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata, SKILL.md frontmatter, manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
