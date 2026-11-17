## Description:

Generates structured A-share stock review reports for midday and full-day analysis, including multidimensional scoring, technical analysis, fundamentals, market context, strategy sections, and risk notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinyan623](https://clawhub.ai/user/martinyan623)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to draft A-share midday or full-day review reports for a named stock and trading date. It is intended to structure analysis and reminders, not to provide verified investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may be mistaken for verified investment advice or current market analysis.

Mitigation: Treat outputs as informational drafts, keep the disclaimer, and independently verify market data and conclusions before acting.

Risk: The included CLI can write files using user-provided stock names and dates.

Mitigation: Use trusted inputs only or sanitize stock names and dates before running the script; verify output paths stay inside the intended reports folder.

Risk: The generator can produce sample reports when real data tools are unavailable or not connected.

Mitigation: Clearly label sample-data outputs and connect or verify real market-data sources before relying on a report.

## Reference(s):

- [Scoring Guide](references/scoring_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/martinyan623/skills/stock-report-generator)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown reports with optional PNG radar chart files and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are named by stock name, report type, and date; full-day reports may add a radar chart.]

## Skill Version(s):

1.0.0 (source: release metadata, _meta.json, CHANGELOG released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
