## Description: <br>
Display session usage statistics (quota, session time, tokens, context) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-drew](https://clawhub.ai/user/c-drew) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to check current Telegram-facing session usage, including API quota, reset timing, token counts, and context usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Clawdbot usage and session data and can invoke the local clawdbot command. <br>
Mitigation: Install and run it only in a trusted local Clawdbot environment with a trusted clawdbot command in PATH. <br>
Risk: Usage statistics sent through Telegram may expose local session, quota, model, provider, or token information. <br>
Mitigation: Share Telegram output only with the intended chat and avoid enabling the command in chats where that operational information should not be visible. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/c-drew/telegram-usage) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Telegram-formatted text or JSON from a Node.js command-line handler] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and a trusted local Clawdbot installation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
