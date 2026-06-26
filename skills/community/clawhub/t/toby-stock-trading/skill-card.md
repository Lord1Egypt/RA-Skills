## Description: <br>
Provides China A-share market data retrieval, individual stock analysis, market sentiment review, sector hotspot tracking, price alerts, and trading strategy suggestions using public finance sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve China mainland A-share market data, summarize technical and fundamental signals, assess broad market sentiment, identify active sectors, and draft risk-aware trading guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading suggestions may be incomplete, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as analytical assistance, include risk notes, and avoid presenting suggestions as guaranteed investment advice. <br>
Risk: The skill makes outbound requests to public finance data providers. <br>
Mitigation: Use it only where those network requests are acceptable and verify market data against trusted sources before acting. <br>
Risk: Price alert workflows may write local watchlist notes. <br>
Mitigation: Do not store brokerage credentials or sensitive account data in watchlist files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tobeyrebecca/toby-stock-trading) <br>
- [Data Sources API Reference](references/data-sources.md) <br>
- [Stock Analysis Method Reference](references/analysis.md) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with concise tables, bullet points, risk notes, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite data source and retrieval time when market data is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
