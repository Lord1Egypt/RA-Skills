## Description: <br>
股智Alpha is an A-share stock screening and analysis skill that combines behavior-finance SLSV signals, RSI/MACD/MA technical indicators, fund-flow signals, and sentiment inputs to score and screen equities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golikegod](https://clawhub.ai/user/golikegod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan A-share equities, analyze individual stocks, and generate scored stock reports, position guidance, and trading-card style summaries for informational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data lookups and generated stock recommendations can be stale, incomplete, unavailable, or misleading. <br>
Mitigation: Treat outputs as informational, verify important quotes and recommendations against trusted financial sources, and keep the skill's investment disclaimer visible in user-facing responses. <br>
Risk: Broad trigger phrases can cause the skill to provide financial recommendations when the user intent is ambiguous. <br>
Mitigation: Confirm the user wants stock-analysis assistance before running scans or making recommendations, especially for portfolio or trading questions. <br>
Risk: The documented scan scope and fund-flow source may not match the default script behavior. <br>
Mitigation: Run the provided script entry points with explicit arguments, report the actual scan scope and data sources used, and surface missing-data warnings instead of hiding degraded inputs. <br>
Risk: The skill performs third-party network requests for market, news, and sentiment data. <br>
Mitigation: Install and run it in an isolated Python environment and avoid providing sensitive account, portfolio, or credential data unless the runtime environment has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golikegod/stock-alpha) <br>
- [Ashare market-data library](https://github.com/mpquant/Ashare) <br>
- [Futu news and sentiment endpoint](https://ai-news-search.futunn.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text reports with tabular summaries, markdown-style sections, and a temporary JSON result file for screeners] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include stock scores, missing-data warnings when available, risk notes, disclaimers, position guidance, and per-stock analysis details.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
