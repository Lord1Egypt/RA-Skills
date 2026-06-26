## Description: <br>
科技新闻日报收集近7天中英文科技与 AI 新闻，去重评分后生成本地 Markdown 报告，并同步到飞书文档和飞书群链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binhuatochina](https://clawhub.ai/user/binhuatochina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compile a daily technology and AI news digest with source links, relevance ratings, recommendation scores, local archive files, and Feishu sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill publishes generated reports to hardcoded Feishu knowledge-base, document, chat, and OpenID targets. <br>
Mitigation: Confirm the Feishu space, parent node, chat, and OpenID belong to the intended operator before running, or replace them with approved destinations. <br>
Risk: The skill grants full document access to a fixed Feishu account. <br>
Mitigation: Review the permission step before execution and reduce or remove the full_access grant unless that account explicitly requires it. <br>
Risk: The fallback Feishu Open API path can use FEISHU_APP_SECRET for tenant token creation. <br>
Mitigation: Use lark-cli where possible, keep FEISHU_APP_SECRET out of generated files and logs, and confirm the app scopes before allowing fallback API calls. <br>
Risk: The generated news report may contain stale, duplicate, or misleading public-news summaries. <br>
Mitigation: Review the report and source links before Feishu upload or group posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binhuatochina/technews-daily-report) <br>
- [飞书文档操作参考](references/feishu-doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report with source links, scoring fields, local file paths, Feishu document links, and checkpoint JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily report files under memory/ and may publish generated document links to configured Feishu destinations.] <br>

## Skill Version(s): <br>
0.3.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
