## Description: <br>
专业采集和分析小红书关键词、笔记、评论和博主数据，支持爆款指标、博主画像、定时跟踪和飞书多维表格输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Suzanneyp](https://clawhub.ai/user/Suzanneyp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, research, and operations users use this skill to collect Xiaohongshu topic and creator data, analyze engagement metrics, identify high-performing content, and organize findings into reports or Feishu tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Xiaohongshu collection may exceed platform limits or collect data without proper authorization. <br>
Mitigation: Install and run only when authorized to collect the data, comply with platform terms, privacy rules, and copyright obligations, and set strict per-run limits. <br>
Risk: Full-content and comment harvesting may capture personal profile details, comments, or copyrighted material. <br>
Mitigation: Avoid collecting full comments or personal profile details unless necessary, minimize stored fields, and review outputs before sharing or reuse. <br>
Risk: Cloud export and scheduled tracking can continue sending collected data after the original task is complete. <br>
Mitigation: Review Feishu destinations and credentials before export, and disable or expire scheduled jobs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Suzanneyp/xiaohongshu-expert) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [小红书全栈专家.md](artifact/å°çº¢ä¹¦å¨æ ä¸å®¶.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown reports, structured tables, Feishu Bitable export instructions, and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Xiaohongshu links, engagement metrics, creator profile fields, comments, and optional Feishu Bitable field mappings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
