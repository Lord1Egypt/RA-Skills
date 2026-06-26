## Description: <br>
基于大虾皮财报命令对上市公司进行ROE/杜邦财务分析，用于单公司财务拆解、ROE驱动分析、盈利质量评估与结构化报告输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to analyze a listed company's financial quality after a stock code is available. It retrieves or accepts financial statement data, applies ROE and DuPont analysis, checks profitability and cash-flow quality, and produces a structured report without giving trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external DaxiAPI CLI and token-based access, so analysis can fail or be incomplete when credentials, permissions, network access, or API responses are unavailable. <br>
Mitigation: Install only if the DaxiAPI service and CLI are trusted, prefer a pinned CLI version when reproducibility matters, avoid sharing real tokens in chat, and pause or narrow the analysis when data retrieval fails. <br>
Risk: Generated financial analysis may be mistaken for investment advice or may overstate conclusions when source data is partial. <br>
Mitigation: Treat outputs as financial analysis rather than buy or sell recommendations, require explicit data-source and limitation notes, and skip unsupported WACC, EVA, peer-ranking, or missing-field conclusions. <br>


## Reference(s): <br>
- [ROE 深度分析框架](references/roe-framework.md) <br>
- [行业分析规则](references/industry-rules.md) <br>
- [报告模板](references/report-template.md) <br>
- [CLI 命令与字段说明](references/cli-commands.md) <br>
- [DaxiAPI](https://daxiapi.com) <br>
- [ClawHub release page](https://clawhub.ai/ksky521/xiapi-financial-roe-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown report with tables and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quick mode targets concise answers; deep mode produces a modular financial analysis report with data-source and limitation notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
