## Description: <br>
Secure webhook token management using MGC Blackbox. Supports DingTalk, WeCom, Feishu, Telegram, Slack and more. Store webhook tokens locally in encrypted form, retrieve at runtime without exposing to AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkeviny](https://clawhub.ai/user/zkeviny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to configure webhook token storage for notification bots and local scripts without exposing secrets to AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook, bot, and MGC tokens can be exposed if users paste them into chat, logs, or shared files. <br>
Mitigation: Install only on a trusted machine, treat all tokens as secrets, avoid sharing tokens in chat or logs, and revoke any token suspected of exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zkeviny/skills/token-safe-webhook-sender) <br>
- [MGC Blackbox](https://github.com/zkeviny/MGC-Blackbox) <br>
- [MGC Blackbox issues](https://github.com/zkeviny/MGC-Blackbox/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code is included in the skill artifact; users configure local MGC Blackbox storage and webhook scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
