## Description: <br>
使用 agent-browser 对 Telegram 机器人进行自动签到，支持通过持久化 Chrome Profile 保留 Telegram Web 登录状态并点击机器人签到按钮。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanbeizizi-max](https://clawhub.ai/user/lanbeizizi-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to drive Telegram Web through agent-browser for recurring bot check-ins, including opening a bot chat, sending commands, selecting the latest check-in button, and capturing screenshots for confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent Chrome profile can retain sensitive Telegram account access. <br>
Mitigation: Treat the profile directory as sensitive, avoid casual backups, and delete or rotate the profile when access should end. <br>
Risk: The watchdog flow can reopen a logged-in Telegram Web session at login or after closure. <br>
Mitigation: Use the on-demand check-in flow unless continuous browser restart behavior is intentional, and unload the launch agent when it is not needed. <br>
Risk: Browser automation may act in the wrong Telegram chat or on an older inline button. <br>
Mitigation: Verify the browser is in the intended bot chat and inspect the latest page snapshot before sending commands or clicking a check-in button. <br>
Risk: Screenshots written to predictable /tmp paths may expose Telegram chat content. <br>
Mitigation: Store screenshots only when needed, review file permissions, and remove temporary screenshot files after verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanbeizizi-max/telegram-checkin) <br>
- [Telegram Web](https://web.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-browser commands, launchd watchdog configuration guidance, and screenshot paths for check-in verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
