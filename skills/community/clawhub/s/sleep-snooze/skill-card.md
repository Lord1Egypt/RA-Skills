## Description: <br>
Snooze incoming notifications during your sleep window and receive a morning digest when you wake up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hardik500](https://clawhub.ai/user/Hardik500) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use this skill to pause non-urgent notifications during configured sleep hours, queue messages locally, and receive a morning digest when they wake. It supports manual sleep and wake commands, setup guidance, urgency bypasses, and provider-agnostic message handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal the user's sleep window to message senders through automatic direct-message replies. <br>
Mitigation: Review or disable the dm-guard auto-reply behavior if disclosing sleep status or schedule information is not acceptable. <br>
Risk: Sleep-time messages and previews are stored locally for later digest generation. <br>
Mitigation: Install only where local storage of message content is acceptable, and review the local data directory and retention expectations before deployment. <br>
Risk: Setup adds persistent cron jobs that control sleep-mode changes and digest delivery. <br>
Mitigation: Review the generated crontab entries after setup and remove or adjust them if the schedule or execution path is not appropriate. <br>


## Reference(s): <br>
- [Sleep Snooze setup guide](references/setup.md) <br>
- [Project homepage](https://github.com/Hardik500/sleep-snooze) <br>
- [ClawHub listing](https://clawhub.ai/Hardik500/sleep-snooze) <br>
- [Publisher profile](https://clawhub.ai/user/Hardik500) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-formatted command output with shell commands for setup and status checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queues message previews locally and emits digest text for delivery through connected OpenClaw providers.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
