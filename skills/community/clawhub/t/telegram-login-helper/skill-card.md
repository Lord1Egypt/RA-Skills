## Description: <br>
Consolidates Telegram personal-account login workflows for tdl/TDLib, including namespace reuse, QR and batch logins, TDLib state transfer, and clear escalation when human authentication or API credentials are required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevewu422](https://clawhub.ai/user/stevewu422) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to recover or set up Telegram personal-account access for local tdl/TDLib workflows without switching to bot tooling. It helps choose between reusing a namespace, QR login, copying an existing session, MTProto fallback, or human-assisted login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusing or copying TDLib session state can expose live Telegram personal-account access if shared, logged, or transferred insecurely. <br>
Mitigation: Treat TDLib state directories like passwords: keep them out of logs and transcripts, restrict file permissions, use secure transfer, and clean up or revoke sessions when needed. <br>
Risk: The workflows can be misused against Telegram accounts the user does not own or have permission to access. <br>
Mitigation: Use the skill only for Telegram accounts you own or are explicitly authorized to manage. <br>
Risk: MTProto fallback requires Telegram API credentials, and QR login requires human authentication when no reusable session is available. <br>
Mitigation: Do not claim login is complete without the required credentials or human step; escalate for one-time authentication when the documented fallback conditions are not met. <br>


## Reference(s): <br>
- [Telegram Login Runbook](references/runbook.md) <br>
- [ClawHub release page](https://clawhub.ai/stevewu422/telegram-login-helper) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require interactive QR login, reusable TDLib session state, or Telegram API credentials depending on the chosen path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
