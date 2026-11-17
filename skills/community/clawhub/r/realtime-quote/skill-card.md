## Description:

Provides Chinese-language A-share market quote tracking guidance for multi-source real-time quotes, latency-aware fallback, Level2 order book data, WebSocket updates, and non-trading-period handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance workflow builders can use this skill to ask an agent for A-share market quote retrieval, source fallback, latency checks, Level2 order book monitoring, and JSON or Markdown reporting guidance. It is aimed at market-data workflows and should not be treated as regulated financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell execution and describes broad command and file handling without clear boundaries.

Mitigation: Install only where local command authority is acceptable, review generated commands before execution, and avoid granting access to private files unless exact file and command boundaries are documented.

Risk: The skill may require market-data API keys or portfolio-related inputs for some workflows.

Mitigation: Provide credentials through environment variables, avoid sharing sensitive portfolio files, and limit API keys to the minimum permissions needed for quote retrieval.

Risk: Market data and generated analysis can be delayed, unavailable, or inconsistent across providers.

Mitigation: Verify important results against licensed market-data sources and apply independent review before trading or investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/realtime-quote)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON examples with command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference market-data API credentials, provider fallback behavior, and generated analysis or monitoring outputs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
