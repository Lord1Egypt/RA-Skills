## Description: <br>
Super Admapix helps agents search ad creatives, analyze apps, inspect rankings, review download and revenue estimates, and produce market intelligence using the AdMapix API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business analysts use this skill to query advertising, app, ranking, download, revenue, and market data in English or Chinese. It supports quick lookups as well as hosted deep research reports for multi-step comparisons and strategy analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured AdMapix API key and business queries to AdMapix services for normal API calls and hosted Deep Research. <br>
Mitigation: Use secure configuration for ADMAPIX_API_KEY, avoid pasting keys into chat, rotate exposed keys, and install only when this data sharing is acceptable. <br>
Risk: Deep Research can produce hosted, shareable reports from sensitive market or competitor-analysis prompts. <br>
Mitigation: Avoid proprietary or confidential prompts unless hosted reports are acceptable, and review whether Deep Research can be disabled or made opt-in in the deployment environment. <br>
Risk: Download and revenue figures are third-party estimates and may not match official or internal data. <br>
Mitigation: Keep the estimate disclaimer visible and validate high-impact decisions against authoritative internal or platform data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-admapix) <br>
- [AdMapix Website](https://www.admapix.com) <br>
- [Creative Search API](artifact/references/api-creative.md) <br>
- [Product and Company API](artifact/references/api-product.md) <br>
- [Ranking API](artifact/references/api-ranking.md) <br>
- [Download and Revenue API](artifact/references/api-download-revenue.md) <br>
- [App Distribution API](artifact/references/api-distribution.md) <br>
- [Market Analysis API](artifact/references/api-market.md) <br>
- [Parameter Mapping Reference](artifact/references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, API-result summaries, tables, links to hosted HTML reports, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses preserve the user's language and include disclaimers when presenting third-party download or revenue estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
