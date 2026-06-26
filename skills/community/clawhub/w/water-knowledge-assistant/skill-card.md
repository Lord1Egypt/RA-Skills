## Description: <br>
水务设备知识库 AI 助手，提供设备查询、选型建议、参数对比等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhulihuaaaaa](https://clawhub.ai/user/zhulihuaaaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, water-operations engineers, and procurement or support teams use this skill to query water-equipment knowledge, compare parameters, receive equipment selection guidance, draft inquiry details, and locate manuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-derived queries may be sent to third-party Tavily and DashScope/OpenAI-compatible services. <br>
Mitigation: Use the skill only when those external services are acceptable, and avoid entering sensitive customer, procurement, or operational details unless an approved data-handling process is in place. <br>
Risk: Audit logs can retain raw inputs, outputs, user identifiers, tool results, and trace data. <br>
Mitigation: Configure log access controls, retention limits, and redaction before production use. <br>
Risk: Cron or on-demand updates can mutate knowledge-base content and add external search summaries. <br>
Mitigation: Disable scheduled or trigger-based updates unless needed, review new knowledge-base files before indexing, and restrict who can start update workflows. <br>
Risk: The ingest workflow can remove destination files that are no longer present in the source hash set. <br>
Mitigation: Run ingestion against a controlled source directory, keep backups of the knowledge-base directory, and review file-prune behavior before enabling automation. <br>


## Reference(s): <br>
- [应用案例](references/application-cases.md) <br>
- [参数术语解释](references/parameter-glossary.md) <br>
- [选型指南](references/selection-guide.md) <br>
- [DashScope OpenAI-compatible API](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>
- [Tavily Search API](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, command-line text, JSONL audit records, and generated knowledge-base files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local knowledge-base files, vector search results, external search summaries, and audit logs when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
