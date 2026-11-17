## Description:

Provides read-only SentiSense sentiment, market mood, smart-money positioning, analyst actions, and AI insight for US stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and market researchers use the skill to review stock sentiment, market mood, and reported insider, congressional, institutional, and analyst activity. It provides educational context from read-only data, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests require a SentiSense key and consume account quota.

Mitigation: Keep a dedicated API key private and mention quota or preview limits when relevant.

Risk: Preview data can be incomplete or delayed, so missing rows do not establish that no activity occurred.

Mitigation: Label preview results with the returned count and total count, and surface data age where available.

## Reference(s):

- [SentiSense API documentation](https://sentisense.ai/skill.md)
- [SentiSense](https://sentisense.ai)
- [ClawHub stock-sentiment release](https://clawhub.ai/thesentitrader/skills/stock-sentiment)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Concise sourced text or Markdown summaries of stock and market sentiment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational context only; not personalized investment advice.]

## Skill Version(s):

0.7.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
