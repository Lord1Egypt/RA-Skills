## Description: <br>
Analyzes stocks and crypto assets through AISA and returns scores, BUY/HOLD/SELL-style signals, confidence, and risk notes when users request ticker analysis, asset comparison, or market-position assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze user-requested stock or crypto tickers through AISA, compare assets, and summarize signals, confidence, and risks. Outputs are informational market analysis and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and analysis prompts are sent to AISA for processing. <br>
Mitigation: Use the skill only when sharing those requested tickers and prompts with AISA is acceptable. <br>
Risk: The skill requires a user-provided AISA_API_KEY and can use a custom AISA_BASE_URL. <br>
Mitigation: Use a dedicated API key, keep it out of prompts and logs, and leave AISA_BASE_URL unset unless the endpoint is intentionally trusted. <br>
Risk: The output may include investment signals, targets, stops, and market commentary. <br>
Mitigation: Treat results as informational market analysis, verify material facts independently, and do not treat the output as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/stock-analysis-zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown market analysis with an optional fenced JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ticker-level scores, signal, confidence, price context, targets, stops, comparison summaries, and risk flags when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
