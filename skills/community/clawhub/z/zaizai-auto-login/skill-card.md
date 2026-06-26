## Description: <br>
自动登录凭据管理，在需要登录时自动填写账号密码，支持 GitHub、知乎、闲鱼、BotStreet 等平台。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[155143783](https://clawhub.ai/user/155143783) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to retrieve and fill login credentials for supported platforms during workflows that require authentication. It is intended for trusted environments where credential access and login actions are explicitly approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes plaintext account credentials and asks agents to use them automatically. <br>
Mitigation: Install only when the publisher is fully trusted, rotate exposed passwords and keys, remove plaintext secrets from the skill and history, and require explicit approval before each credential retrieval or login. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/155143783/zaizai-auto-login) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow guidance for credential retrieval, browser form filling, and manual user handoff for verification challenges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
