## Description: <br>
将任务执行结果推送到负一屏卡片显示，支持普通推送和定时任务推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pingjiang](https://clawhub.ai/user/pingjiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to send agent task results to a mobile Today-screen card, including immediate conversation results and scheduled task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent outputs may leave the local environment through an external phone notification service. <br>
Mitigation: Use only for non-confidential content unless the destination API URL, auth-code handling, and data retention expectations are understood. <br>
Risk: Scheduled task results can be pushed automatically without a fresh user confirmation. <br>
Mitigation: Disable or tightly control scheduled pushes when automatic delivery is not appropriate. <br>
Risk: Authentication is controlled by AS_TODAY_AUTH_CODE. <br>
Mitigation: Store the auth code only in the skill environment configuration and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pingjiang/push2today) <br>
- [Publisher profile](https://clawhub.ai/user/pingjiang) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and AS_TODAY_AUTH_CODE; sends summarized task results and content to a configured phone notification API.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
