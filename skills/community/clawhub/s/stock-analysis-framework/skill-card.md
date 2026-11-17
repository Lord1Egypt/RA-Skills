## Description:

Stock Analysis Framework provides a six-dimension A-share stock analysis workflow and monitoring utilities for fundamentals, technicals, news, capital flows, sentiment, and macro policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate structured A-share stock analysis, monitor holdings, and produce portfolio briefings. It is intended as an informational analysis aid rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried ticker symbols and portfolio holdings may be sent to third-party market-data services during quote retrieval.

Mitigation: Run only in environments where sharing those symbols is acceptable, and review local portfolio files before using monitoring or briefing scripts.

Risk: Generated reports, alerts, and summaries may be mistaken for investment advice.

Mitigation: Treat all outputs as informational inputs and require human review before making trading decisions.

## Reference(s):

- [Fundamental Analysis Guide](artifact/references/fundamental.md)
- [Technical Analysis Guide](artifact/references/technical.md)
- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/stock-analysis-framework)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style console reports and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live market quotes, portfolio summaries, alerts, and informational stock-analysis guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
