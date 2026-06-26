## Description: <br>
Helps agents onboard Telegram groups by discovering blocked group chat IDs, updating OpenClaw configuration, creating group project files, and verifying bot responsiveness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to make a Telegram bot respond in newly created groups and to set up per-group project files after the group is added. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can configure Telegram groups so the bot responds to all group messages without requiring mentions. <br>
Mitigation: Use allowlist or requireMention=true unless broad group access is intentional, and confirm the target group before applying changes. <br>
Risk: The workflow can modify local or remote OpenClaw configuration. <br>
Mitigation: Confirm the exact server and chat ID, review the configuration change and backup, and run remote commands only on trusted hosts. <br>
Risk: Group project setup may create persistent knowledge files that influence future responses. <br>
Mitigation: Restrict who can add persistent project knowledge and review project files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/moltbotmolty-del/telegram-group-onboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local or remote shell commands and project file content for Telegram group onboarding.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
