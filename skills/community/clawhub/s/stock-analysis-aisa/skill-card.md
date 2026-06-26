## Description: <br>
Analyze stocks and cryptocurrencies with live AISA-backed scoring, signals, confidence, and risk flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze stock and cryptocurrency tickers, compare assets, and produce informational scoring, signals, confidence, and risk flags through an AISA-backed Python workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends analysis requests to an external AISA-compatible API. <br>
Mitigation: Use a dedicated AISA_API_KEY, verify AISA_BASE_URL before overriding it, and avoid sending sensitive portfolio details unless intended. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Store AISA_API_KEY in an environment variable or secret manager, scope it for this workflow, and rotate it if exposed. <br>
Risk: Financial analysis output may be incomplete, incorrect, or unsuitable as investment advice. <br>
Mitigation: Treat recommendations as informational, verify live market data independently, and rely on qualified financial judgment before making decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/stock-analysis-aisa) <br>
- [Publisher profile](https://clawhub.ai/user/bibaofeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with optional fenced JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and AISA_API_KEY; accepts one or more stock or crypto tickers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
