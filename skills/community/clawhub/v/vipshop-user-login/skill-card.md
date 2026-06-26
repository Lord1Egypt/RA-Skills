## Description: <br>
Vipshop QR-code login skill that lets an agent obtain and display a login QR code, poll for user confirmation, and save reusable Vipshop session cookies for other Vipshop skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viphgta](https://clawhub.ai/user/viphgta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs authenticated access to Vipshop workflows. It guides the user through QR-code login, polls for confirmation, and stores the resulting session for later Vipshop skill use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Vipshop account cookies in ~/.vipshop-user-login/tokens.json, and other Vipshop skills can read and use that session. <br>
Mitigation: Install only on a trusted machine, treat the file as an account credential, and remove it with the documented logout command or by deleting the directory when access is no longer needed. <br>


## Reference(s): <br>
- [Vipshop QR Login API Reference](artifact/references/api_reference.md) <br>
- [Vipshop Skill Integration Guide](artifact/references/integration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown QR image display, CLI text, machine-readable JSON payloads in stdout, and a local JSON credential file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores reusable Vipshop cookies in ~/.vipshop-user-login/tokens.json for other Vipshop skills.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
