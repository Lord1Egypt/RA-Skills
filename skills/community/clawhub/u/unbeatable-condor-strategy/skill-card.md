## Description:

Checks whether requested stock tickers meet a 4% volatility threshold for an options condor signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinntrance](https://clawhub.ai/user/jinntrance)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check selected equity tickers for a daily options condor or strangle signal and summarize the reported sell-strike thresholds. Its outputs should be treated as informational trading analysis, not as authorization to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce direct options-trading instructions that may be mistaken for financial advice.

Mitigation: Treat all results as informational analysis and require a qualified human review before any trade decision.

Risk: An agent could place trades or allocate capital based only on the generated signal.

Mitigation: Do not grant trading or capital-allocation authority to the agent based on this output.

Risk: The skill downloads current market data and runs local Python dependencies.

Mitigation: Review the code before installation and run it only in an isolated Python environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinntrance/skills/unbeatable-condor-strategy)
- [ClawHub publisher profile](https://clawhub.ai/user/jinntrance)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise trading-signal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include signal status, put and call strike thresholds, abstention guidance, and risk reminders.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
