## Description:

Uses Tavily-powered search to retrieve and summarize gold market information across Chinese and international venues, including spot prices, technical indicators, fundamentals, and risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmouseboy](https://clawhub.ai/user/fmouseboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather current gold-market search results and produce a concise analysis report covering price overview, technical signals, fundamentals, and investment-risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gold-market searches are sent to Tavily using the user's TAVILY_API_KEY.

Mitigation: Avoid including secrets, account details, private trading plans, or other sensitive information in queries.

Risk: Investment analysis may be incomplete, stale, or unsuitable for a user's financial situation.

Mitigation: Treat output as informational only and review it with current market data and appropriate financial judgment before acting.

## Reference(s):

- [Sudu Gold ClawHub page](https://clawhub.ai/fmouseboy/skills/sudu-gold)
- [Publisher profile](https://clawhub.ai/user/fmouseboy)
- [Gold Technical Indicators Reference](references/technical-indicators.md)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style analysis report with sourced search results and console text from the Node.js script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; sends search queries to Tavily.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
