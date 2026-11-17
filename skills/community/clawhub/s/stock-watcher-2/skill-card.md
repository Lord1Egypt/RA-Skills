## Description:

Stock Watcher is a stock monitoring and alerting skill for watchlists, using cost, price-change, volume, moving-average, RSI, gap, and trailing-stop rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandelion80231](https://clawhub.ai/user/dandelion80231)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run stock, ETF, and gold watchlist monitoring, generate alerts from technical and position-based rules, and review supporting market summaries. Outputs should be treated as monitoring aids rather than professional investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat monitoring alerts or generated market suggestions as professional investment advice.

Mitigation: Use outputs as informational signals, verify them against independent market data, and consult a qualified professional before trading.

Risk: Long-lived monitoring may use locally stored watchlists, cost basis, and portfolio configuration.

Mitigation: Store only portfolio data you are comfortable keeping locally, protect configuration files, and review data-source integrations before daemon use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dandelion80231/skills/stock-watcher-2)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and Python configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include alert messages, technical indicator summaries, and risk guidance; not investment advice.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
