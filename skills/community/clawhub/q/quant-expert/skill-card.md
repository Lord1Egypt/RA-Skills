## Description: <br>
Quantitative analysis skill for the Chinese A-share market using Tushare Pro data and a holiday helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Noah-Wu66](https://clawhub.ai/user/Noah-Wu66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and OpenClaw users use this skill to query Tushare data, screen Chinese A-share securities, diagnose individual stocks, check Chinese trading days, and combine quantitative findings with event context when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tushare token for most bundled scripts. <br>
Mitigation: Keep the token outside the repository and provide it through the configured TUSHARE_TOKEN environment mapping. <br>
Risk: The skill can query external services, including Tushare, timor.tech, and web sources used for market context. <br>
Mitigation: Install and run it only in environments where those outbound queries are acceptable for the user's data-handling requirements. <br>
Risk: Some scripts support user-directed output files that may create or overwrite paths. <br>
Mitigation: Use output-file options only with paths intended for generated reports or exports. <br>
Risk: Financial prompts may include confidential holdings, watchlists, or proprietary strategies. <br>
Mitigation: Avoid sharing sensitive portfolio or strategy details when requesting web-backed recommendations or interpretations. <br>


## Reference(s): <br>
- [Quant-Expert ClawHub Page](https://clawhub.ai/Noah-Wu66/quant-expert) <br>
- [Tushare Pro API Quick Reference](references/api_quick_reference.md) <br>
- [Quantitative Analysis Strategies](references/analysis_strategies.md) <br>
- [timor.tech Holiday API](https://timor.tech/api/holiday/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands, JSON snippets, and CSV or Markdown file exports from bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Tushare query results, stock screening tables, diagnosis reports, trading-day checks, and event-backed investment context when web research is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
