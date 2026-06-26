## Description: <br>
Aggregates WeChat public-account content from names or links, summarizes account positioning and key viewpoints, records keyword preferences, and prepares scheduled content digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to understand what a WeChat public account covers, choose keyword preferences, receive daily aggregated summaries, and optionally save approved summaries to a Feishu content library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public-account names or links may be searched through Baidu. <br>
Mitigation: Avoid submitting sensitive or private account links, and review what will be searched before using the skill. <br>
Risk: Keyword preferences may be remembered and used for daily push behavior. <br>
Mitigation: Confirm the selected preferences and schedule, and update or clear remembered preferences when they are no longer appropriate. <br>
Risk: Approved summaries may be exported to a Feishu table. <br>
Mitigation: Use limited Feishu permissions and confirm the destination table before saving records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/zhuchenggong-wechat-account-aggregation) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown summaries with table-style account fields and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remembered keyword preferences, daily 10:00 push behavior, and optional Feishu record creation after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
