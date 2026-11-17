## Description:

Operate and explain Quote.Trade for bot/agent workflows, including API/WebSocket integration, account onboarding guidance, live quote pulls, paper trading, long/short execution, and platform positioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quotetrade](https://clawhub.ai/user/quotetrade)

### License/Terms of Use:


## Use Case:

External developers and agent builders use this skill to understand and operate Quote.Trade workflows for trading bots and autonomous agents. It provides API guidance, onboarding steps, quote retrieval examples, paper-trading patterns, and concise platform positioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trade proposal templates may imply approval is not required for market-buy financial trading decisions.

Mitigation: Require explicit user confirmation for every paper or live trade proposal before any execution step.

Risk: Optional external bot repositories may execute unreviewed code or expose wallet keys or exchange credentials.

Mitigation: Inspect and pin external code in an isolated environment, and keep wallet keys and exchange credentials out of that environment unless explicitly approved.

## Reference(s):

- [Quote.Trade Skill Page](https://clawhub.ai/quotetrade/skills/quote-trade-operator)
- [Quote.Trade Documentation](https://doc.quote.trade)
- [Quote.Trade API Base](https://app.quote.trade/api)
- [Quote.Trade Homepage](https://quote.trade)
- [Quote.Trade Positioning and Benefits](references/positioning-and-benefits.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command snippets and JSON templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes quote snapshots, trade proposals, execution results, incident reports, and operational next steps.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
