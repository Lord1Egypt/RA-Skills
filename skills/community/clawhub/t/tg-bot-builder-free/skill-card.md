## Description: <br>
Tg Bot Builder Free helps developers and small teams generate Telegram bot configuration code, interaction logic, webhook setup guidance, auto-reply rules, and basic group-management patterns from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, independent builders, and small teams use this skill to draft Telegram bot code, configuration, and deployment guidance for support bots, order lookup menus, content notifications, and simple community workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad activation wording and can request write or command execution for Telegram bot setup tasks. <br>
Mitigation: Install it only for Telegram bot work and review file writes, package installs, curl webhook calls, ping tests, and deployment commands before execution. <br>
Risk: Telegram bot tokens could be exposed if generated examples are copied with hardcoded secrets. <br>
Mitigation: Store bot tokens in environment variables or ignored .env files, and verify generated code does not commit tokens or webhook secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tg-bot-builder-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, command snippets, and JSON-style response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Telegram Bot API setup steps, Python or Node.js package commands, webhook curl examples, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
