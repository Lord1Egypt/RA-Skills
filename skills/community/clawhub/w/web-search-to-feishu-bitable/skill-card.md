## Description: <br>
自动搜索关键词网页内容，提取标题、摘要、标签和分类等信息，并批量整理到飞书多维表格个人知识库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mildnes](https://clawhub.ai/user/mildnes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
个人知识管理用户和知识工作者可用此技能按关键词收集网页资料，生成摘要、标签和分类，并将结果写入飞书多维表格。它适合整理技术文章、AI 提示词资料和专题资料集合。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the user's Feishu authorization to create or append Bitable records. <br>
Mitigation: Ask the agent to preview the target app, table, fields, and rows before importing into important workspaces. <br>
Risk: Web search summaries and classifications may be incomplete or inaccurate. <br>
Mitigation: Review generated summaries, tags, categories, and source URLs before relying on the knowledge base. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mildnes/web-search-to-feishu-bitable) <br>
- [Publisher profile](https://clawhub.ai/user/mildnes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text status updates with structured Bitable fields and a Feishu link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends Feishu Bitable records with title, URL, summary, tags, and category fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-04-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
