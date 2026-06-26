## Description: <br>
Controls Xiaomi Mi Home smart devices such as lights, air conditioners, and robot vacuums through Xiaomi IoT account access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanlan314](https://clawhub.ai/user/lanlan314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home automation users and agents use this skill to log in to a Xiaomi account, discover Mi Home devices, query device status, trigger scenes, and issue device control requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide Xiaomi account passwords and verification codes through chat or a Feishu workflow. <br>
Mitigation: Use only if that credential flow is acceptable; prefer a dedicated low-privilege Xiaomi account and avoid accounts that protect sensitive home devices. <br>
Risk: Reusable Xiaomi tokens are cached locally with weak safeguards. <br>
Mitigation: Restrict access to the token cache, delete it when no longer needed, and keep the OpenClaw skill data directory permissions limited to the local user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanlan314/xiaomi-miot-lan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text responses with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include device lists, login prompts, captcha prompts, status messages, and setup instructions.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
