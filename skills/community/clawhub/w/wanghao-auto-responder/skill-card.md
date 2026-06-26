## Description: <br>
王昊自动回复助手用于帮王昊自动响应同事的业务咨询，支持定时扫描、手动触发和未完成事项查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to monitor Feishu private chats and group mentions for Wang Hao, answer routine business, process, product, and team-data questions from internal knowledge sources, and record replies for follow-up summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can monitor Feishu private chats and group mentions and send replies without Wang Hao approving each response. <br>
Mitigation: Configure chat and source allowlists, require approval for sensitive or uncertain replies, and limit auto-reply scope to routine business questions. <br>
Risk: Attachment or voice transcription can expose internal or personal content. <br>
Mitigation: Restrict or sandbox attachment transcription and skip sensitive, personal, complaint, or approval-related messages. <br>
Risk: Reply logs may retain message content and sender details. <br>
Mitigation: Set short retention and redaction rules for memory/wanghao-auto-responder.md and limit access to the log. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/runkecheng/wanghao-auto-responder) <br>
- [线上业务知识库索引](https://sqb.feishu.cn/docx/KsvYdfpKNoVt8VxooeBceTpenAg) <br>
- [追光学习文件汇总](https://sqb.feishu.cn/docx/Hp9Ed5R1to6fgyxIggDcB5G5nSd) <br>
- [更新宣导（产品更新日志）](https://sqb.feishu.cn/base/PqnpbUhcxaXo8VsCl2DcVoiJnIN) <br>
- [办公指南（内部知识库）](https://sqb.feishu.cn/wiki/AhLmw2dJmimgtMkQcJ0cQU5Wn8e) <br>
- [品牌资源总入口](https://sqb.feishu.cn/wiki/CTMpwoqgjiAMBYkaDLIcTKOfn4g) <br>
- [AI应用知识库](https://sqb.feishu.cn/wiki/II5KwmDZUi38OdkjiZbchb8TnKc) <br>
- [全来店SaaS销售指南](https://sqb.feishu.cn/wiki/LwY3whLj9iIAzqkWCIOcFHGDn2e) <br>
- [产品更新及项目发布（月度）](https://sqb.feishu.cn/sheets/JcxtsI68OhUOIrtjsQmcXbQbnlm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Feishu reply payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replies are intended to be concise, at most 300 Chinese characters, and include source references when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
