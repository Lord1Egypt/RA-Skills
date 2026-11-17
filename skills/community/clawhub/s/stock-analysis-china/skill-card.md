## Description:

Analyzes China A-share portfolio screenshots or saved holdings, updates portfolio data, retrieves AKShare market data, calculates technical indicators, and returns structured holding diagnostics with action suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzwaang](https://clawhub.ai/user/lzwaang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn China A-share portfolio screenshots or saved holdings into a technical-analysis report. It supports portfolio updates, market and index lookup, indicator calculations, and suggested hold, reduce, add, take-profit, or stop-loss actions for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read inbound local screenshots, including screenshots that may not be intended for portfolio analysis.

Mitigation: Require explicit user confirmation before processing images and verify that the selected screenshot is portfolio-related.

Risk: The skill can overwrite, remove, or clear stored portfolio holdings.

Mitigation: Confirm the recognized holdings and requested portfolio changes before writing positions_portfolio.json or clearing entries.

Risk: The skill includes guidance for broad environment changes and global or system package installation.

Mitigation: Review setup commands before execution and avoid running global or system install commands automatically.

Risk: The generated stock analysis may be incomplete or misleading if market data, OCR, or technical indicators are inaccurate.

Mitigation: Treat reports as informational technical analysis, verify source data, and do not treat action suggestions as financial advice.

## Reference(s):

- [Analysis prompt template](references/analysis_prompt_template.md)
- [ClawHub skill page](https://clawhub.ai/lzwaang/skills/stock-analysis-china)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style chat report with optional shell commands and JSON portfolio updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read inbound portfolio screenshots, update positions_portfolio.json, fetch live market data through AKShare, and print structured analysis results.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
