## Description:

Structured research process for generating and stress-testing trading ideas from the full macro picture instead of the latest headline. Use when the user asks for trade ideas, a market outlook, "what should I look at", a thesis check on a ticker or theme, or a review of an open position's thesis. Produces idea cards with thesis, stop, exit conditions and event risk, and keeps an idea log so ideas can be scored later. Works on its own with web search; optionally records ideas in the Trading Journal skill. Research aid, not financial advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximsinyaev](https://clawhub.ai/user/maximsinyaev)

### License/Terms of Use:

MIT-0

## Use Case:

Individual investors and market researchers use this skill to structure macro-driven trading research, test theses against counter-evidence, define invalidation and exit conditions, and track ideas for later review. It is a research aid and does not provide personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial: four referenced local paths could not be resolved, so their effects were not verified.

Mitigation: Review the skill instructions and any local settings or files it references before relying on it.

Risk: The scan reports a low-confidence concern about autonomous decision-making, and a benign verdict does not mean risk-free.

Mitigation: Treat idea cards as research aid; verify sources and assumptions, and keep decisions and position sizing within the user's stated rules.

## Reference(s):

- [Macro scan checklist](artifact/references/macro-checklist.md)
- [Bias checklist](artifact/references/bias-checklist.md)
- [Research brief](artifact/references/research-brief.md)
- [Idea report and card template](artifact/references/output-template.md)
- [Position review guide](artifact/references/position-review.md)
- [Idea log and scoring guide](artifact/references/idea-log.md)
- [Trading Journal handoff guide](artifact/references/journal-handoff.md)
- [Financial research disclaimer](artifact/references/disclaimer.md)
- [ClawHub skill release](https://clawhub.ai/maximsinyaev/skills/trading-idea-analyst)
- [Project homepage (skill metadata)](https://github.com/MaximSinyaev/agent-trading-journal)
- [v1.3.0 release notes](https://github.com/MaximSinyaev/agent-trading-journal/releases/tag/v1.3.0)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown research reports with structured idea cards and a machine-readable JSON line per idea]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes thesis evidence and counter-evidence, reference prices with timestamps and sources, risk controls, and exit conditions.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
