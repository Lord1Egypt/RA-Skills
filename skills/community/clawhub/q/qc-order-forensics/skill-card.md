## Description:

Forensic diagnosis engine for backtest order data -- trade quality, ROI attribution, monthly cashflow, drawdown root-cause analysis, and LLM-readable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tltby12341](https://clawhub.ai/user/tltby12341)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative strategy researchers use this skill to analyze QuantConnect backtest order exports and understand trade quality, ROI attribution, monthly cashflow, yearly performance, and drawdown streaks. The generated report is intended to support follow-up strategy analysis by an agent or LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may carry untrusted prompt text from backtest exports into a downstream LLM workflow.

Mitigation: Use only trusted backtest exports and treat generated reports as untrusted content when passing them to another model.

Risk: ROI, cashflow, yearly, and drawdown outputs may be materially misleading because the scanner identified sell-cashflow sign logic concerns.

Mitigation: Do not rely on these calculations for decisions until the cashflow logic is fixed, reviewed, and tested against known expected results.

Risk: Dependencies are specified with lower bounds rather than pinned reviewed versions.

Mitigation: Install pandas and numpy from pinned, reviewed versions in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tltby12341/skills/qc-order-forensics)
- [Publisher profile](https://clawhub.ai/user/tltby12341)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact forensic analysis script](artifact/forensics.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain-text diagnostic report with Markdown-compatible sections and optional Python or shell usage snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes a standard QuantConnect orders.csv file and optionally a result.json file; reports should be treated as untrusted when passed to another LLM.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
