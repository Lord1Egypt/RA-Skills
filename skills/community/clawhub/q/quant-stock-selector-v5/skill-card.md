## Description: <br>
三层筛网量化选股v1.0 helps an agent run an A-share stock screening workflow that filters candidates, scores them with value, quality, and momentum factors, and returns an industry-balanced shortlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-oriented developers use this skill to screen A-share equities with a three-layer process: hard exclusions, multi-factor scoring, and industry balance. Outputs are informational screening results and are not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact embeds and automatically uses a third-party JQData credential. <br>
Mitigation: Remove and rotate the exposed credential before use, and require users to provide credentials through environment variables or secure configuration. <br>
Risk: The skill produces stock-screening results that could be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational screening only, review the assumptions and data freshness, and require human financial judgment before any trading decision. <br>
Risk: Recurring execution can repeatedly call finance data services and generate scheduled screening outputs. <br>
Mitigation: Enable scheduled runs only when the operator intentionally wants recurring finance scans and has reviewed service terms, credentials, and output handling. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paudyyin/quant-stock-selector-v5) <br>
- [Original strategy article](https://zhuanlan.zhihu.com/p/1996940902648796995) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Markdown, Code] <br>
**Output Format:** [Console text and markdown guidance with tabular stock-screening results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires third-party market data packages and data-service credentials before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
