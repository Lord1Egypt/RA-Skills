## Description: <br>
Evaluates stock dividend yield, payout safety, dividend growth, coverage, and income quality through the AISA API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request dividend-income analysis for stocks, including yield, payout safety, dividend growth, coverage, safety scoring, and multi-ticker comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker prompts and dividend-analysis requests are sent to an external AISA-compatible API using AISA_API_KEY. <br>
Mitigation: Install only if you trust the AISA service, keep AISA_API_KEY secret, and avoid sending sensitive portfolio details unless intended. <br>
Risk: AISA_BASE_URL can redirect requests to a different endpoint if overridden. <br>
Mitigation: Verify any AISA_BASE_URL override before running the skill and leave the default endpoint in place unless a trusted alternative is intended. <br>
Risk: Dividend analysis may be mistaken for investment advice. <br>
Mitigation: Treat the output as informational financial analysis and independently verify data before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/stock-dividend-zh) <br>
- [AISA API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown dividend analysis with tables and an optional JSON summary block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and AISA_API_KEY; can compare multiple ticker symbols and can append a structured JSON summary when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
