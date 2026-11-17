## Description:

Screens A-share market data for limit-up and strong-performing stocks, including ChiNext and STAR Market filters and sector limit-up counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrblackerx](https://clawhub.ai/user/mrblackerx)

### License/Terms of Use:


## Use Case:

External users, traders, and market analysts can use this skill to screen Chinese A-share market movers and review limit-up candidates and sector counts. Outputs should be treated as market screening data, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool calls East Money live quote endpoints while the artifact documentation names Sina Finance.

Mitigation: Confirm the live data provider and endpoint behavior before relying on results or documenting the source.

Risk: The output is Chinese-only market screening data and may be mistaken for investment advice.

Mitigation: Present results as informational screening data and require human financial judgment before any trading decision.

Risk: Remote quote responses are not size-limited and timed-out requests are not fully aborted.

Mitigation: Run in an environment with network controls and add response-size limits and request abort handling before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrblackerx/skills/stock-board)
- [Artifact skill description](artifact/SKILL.md)
- [East Money quote API endpoint](https://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output, often summarized in Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language stock screening results based on live public market data.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
