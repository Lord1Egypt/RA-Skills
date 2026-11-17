## Description:

Answers stock research requests with compact, sourced market views and provides a staged guide to building a local chat-and-canvas terminal when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Market researchers use it to gather and summarize sourced, read-only views of stock prices, sentiment, news, filings, analyst activity, earnings, and end-of-day options data. Developers can use its contracts and staged guide to build a local chat-and-canvas terminal when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict with medium confidence, but some files were not fully inspected and runtime permission evidence is unavailable.

Mitigation: Review the artifact sources before deployment and keep network access within the documented HTTPS SentiSense endpoint.

Risk: The skill uses SENTISENSE_API_KEY to authenticate market-data requests.

Mitigation: Keep the key in the runtime environment; do not print it or place it in URLs, artifacts, or renderer code.

## Reference(s):

- [SentiSense API reference](https://sentisense.ai/skill.md)
- [SentiSense API key setup](https://app.sentisense.ai/get-api-key)
- [Stock Terminal on ClawHub](https://clawhub.ai/thesentitrader/skills/stock-terminal)
- [Commands and data recipes](references/commands-and-data.md)
- [Build in an afternoon](references/build-in-an-afternoon.md)
- [Canvas grammar](references/canvas-grammar.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Code, XML]

**Output Format:** [Sourced Markdown screens or concise text; requested local app builds may include code and validated XML canvas artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market observations retain available source dates, coverage, and preview status; missing data is presented as unavailable.]

## Skill Version(s):

2.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
