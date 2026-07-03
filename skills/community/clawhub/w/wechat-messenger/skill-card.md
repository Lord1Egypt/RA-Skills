## Description: <br>
Send WeChat messages via direct Win32 API in about two seconds per message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users with WeChat PC running and logged in can ask an agent to send a specific message to a named contact from the local desktop session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can immediately send real WeChat messages from the user's logged-in account without a confirmation step. <br>
Mitigation: Verify the target contact and message before execution, and add a confirmation or dry-run step before using it in higher-risk workflows. <br>
Risk: The skill takes over WeChat focus and uses mouse, keyboard, and clipboard automation, so desktop activity during execution can affect where input is sent. <br>
Mitigation: Keep WeChat open and avoid using the computer while the command runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chen6896qqwee/skills/wechat-messenger) <br>
- [Publisher profile](https://clawhub.ai/user/chen6896qqwee) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat PC to be running and logged in, with pywin32 and pyperclip installed.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
