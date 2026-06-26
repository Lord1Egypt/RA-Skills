## Description: <br>
1Password-backed credential filling via vault_suggest/vault_fill plugin tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moodykong](https://clawhub.ai/user/moodykong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide agent-driven browser login flows that fill credentials through approved 1Password-backed plugin tools while keeping secrets out of the agent conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to help with real browser logins and credential autofill. <br>
Mitigation: Use it only for sites and accounts the user has confirmed, and confirm the destination before submitting credentials. <br>
Risk: A 1Password service account token or gateway environment file may contain sensitive secrets. <br>
Mitigation: Use a least-privilege token when needed, avoid pasting tokens into chat, and protect env files that store secrets. <br>
Risk: The installation guidance includes sudo commands for installing Google Chrome on WSL. <br>
Mitigation: Review privileged install commands before running them and execute them only in the intended environment. <br>
Risk: The autofill plugin types asynchronously, so submitting too quickly may use incomplete field values. <br>
Mitigation: Wait about one second after vault_fill before clicking submit, as documented by the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/moodykong/secure-autofill) <br>
- [OpenClaw project homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is user-directed and expects external plugin tools for credential lookup and filling.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
