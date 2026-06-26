## Description: <br>
ZDAT评论互动技能。话术库智能匹配回复+线索台账自动写入+主动拓流互动限流。支持知乎/小红书/微博等平台评论管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freemanyg](https://clawhub.ai/user/freemanyg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External social-media operators and marketing teams use this skill to inspect comments, match scenario-based reply language, identify high-intent inquiries, record leads, and generate daily interaction reports for platforms such as Zhihu, Xiaohongshu, and Weibo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for automated public replies and scheduled external interaction without clear approval boundaries. <br>
Mitigation: Use only on accounts and platforms where automated replies are allowed, configure narrow triggers, and require explicit approval before posting replies. <br>
Risk: High-intent commenter details may be written to a lead ledger. <br>
Mitigation: Limit recorded data to what is necessary, restrict ledger access, and confirm the organization has appropriate data-handling approval. <br>
Risk: Automated activity can affect external platform accounts if limits or policies are exceeded. <br>
Mitigation: Keep platform-specific daily limits enabled, monitor daily reports, and stop automation when review or policy uncertainty arises. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freemanyg/zdat-chat-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown or console text with Python command examples and optional spreadsheet ledger updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write high-intent commenter details to clue_ledger.xlsx and print daily summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
