## Description: <br>
分析和总结URL链接内容，并保存到obsidian中，同时定期提醒复习 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nbutmickey](https://clawhub.ai/user/nbutmickey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect URL content, generate summaries, tags, and categories, save notes as Markdown for Obsidian, and schedule spaced review reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched page text may be sent to DeepSeek for summarization. <br>
Mitigation: Use only URLs whose extracted content is acceptable to send to DeepSeek, and provide a least-privilege API key. <br>
Risk: Markdown files can be modified without strong path containment around item IDs. <br>
Mitigation: Configure the Obsidian storage path carefully and avoid untrusted item IDs until path validation is added. <br>
Risk: The optional OpenClaw cron job can run daily automatic review updates. <br>
Mitigation: Enable the cron job only when daily scheduled review reminders are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nbutmickey/smart-collect) <br>
- [DeepSeek API endpoint](https://api.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, terminal text, JSON snippets, and cron configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates Markdown collection records and review metadata in a configured Obsidian storage path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
