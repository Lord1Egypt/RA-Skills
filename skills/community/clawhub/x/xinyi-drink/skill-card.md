## Description: <br>
Helps users claim the xinyi-drink Skill gift pack, review personal order history, check menu and calorie information, and look up store wait times for 新一好喝/新一咖啡. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[domilin](https://clawhub.ai/user/domilin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users of 新一好喝/新一咖啡 use this skill to claim Skill user rewards, ask about their own order history and drink preferences, inspect menu or calorie details, and check store wait times. The skill can run local Python scripts, call the configured Xinyi backend, and use an optional user-provided or saved phone number for reward and order workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reward and order workflows can send the user's 新一咖啡 bound phone number to the configured backend. <br>
Mitigation: Use only the user's own phone number, require explicit reward or order intent, and avoid these workflows when the user asks to use someone else's number. <br>
Risk: The skill can save a phone number and activity status in a local state file, which may be exposed on shared machines or shared agent profiles. <br>
Mitigation: Clear the cache with the documented clear-mobile command after use on shared machines, and rely on the 0600 state-file permission behavior where supported. <br>
Risk: Overriding XINYI_API_BASE_URL can redirect phone number, activity, and order context to an untrusted server. <br>
Mitigation: Do not override XINYI_API_BASE_URL unless the destination server is trusted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/domilin/xinyi-drink) <br>
- [Project homepage](https://github.com/xinyi-drink/xinyi-drink) <br>
- [能力地图](references/capability-map.md) <br>
- [隐私边界](references/privacy-boundaries.md) <br>
- [意图路由](references/intent-routing.md) <br>
- [活动流程](references/activity-flow.md) <br>
- [回答规范](references/response-guidelines.md) <br>
- [平台安装说明](references/platform-install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text, with shell commands for local script execution when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include store tables, order summaries, reward status, menu context, and privacy-preserving guidance based on backend responses.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
