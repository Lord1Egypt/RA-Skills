## Description: <br>
Provides a Vipshop QR-code login flow that shows a scannable login QR code, polls for confirmation, and saves the resulting session cookies for other Vipshop skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vip](https://clawhub.ai/user/vip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to authenticate a Vipshop account through QR-code scanning so other Vipshop workflows can reuse the saved session. Developers can also use its scripts and integration guide to add QR-login and cookie reuse to related Vipshop skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable Vipshop account cookies are saved locally and can be read by other Vipshop skills. <br>
Mitigation: Install only from a trusted publisher, use trusted companion skills, treat ~/.vipshop-user-login/tokens.json as a login credential, and delete it or run logout when session reuse is no longer wanted. <br>
Risk: The QR-login flow creates a real authenticated Vipshop session. <br>
Mitigation: Use the skill only when the user intentionally starts Vipshop login, show the QR image directly for user verification, and avoid shared machines for account sessions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vip/vip-login) <br>
- [Vipshop QR login API reference](references/api_reference.md) <br>
- [Vipshop login integration guide](references/integration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown QR image instructions, text status messages, machine-readable JSON QR payload, and a local JSON cookie file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores reusable Vipshop session cookies at ~/.vipshop-user-login/tokens.json for use by related skills.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
