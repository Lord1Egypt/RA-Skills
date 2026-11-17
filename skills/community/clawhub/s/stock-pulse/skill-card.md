## Description:

A-share stock analysis dashboard that accepts stock codes and produces buy, sell, or hold signals, exact price points, day charts, Monte Carlo month/year price forecasts, and combined buy recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vineindalvik](https://clawhub.ai/user/vineindalvik)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze A-share stock codes, inspect recent price movement, generate month or year price forecasts, and receive concise trading posture guidance. Outputs should be treated as informational market analysis rather than financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives concrete trading recommendations that may be incorrect, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as informational analysis only and require human review before making investment decisions.

Risk: Stock codes, prompts, generated analysis, and webhook messages may be sent to configured external services.

Mitigation: Run in an isolated environment, use a dedicated low-privilege LLM key, set LLM_BASE_URL only to a trusted HTTPS provider, and enable webhooks only when their destination is approved.

## Reference(s):

- [baostock data source](http://baostock.com/)
- [ClawHub skill page](https://clawhub.ai/vineindalvik/skills/stock-pulse)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown-style console text, JSON from internal LLM analysis prompts, ASCII charts, and optional webhook text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires stock code inputs, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, and network access to the configured LLM provider and baostock data source.]

## Skill Version(s):

1.2.5 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
