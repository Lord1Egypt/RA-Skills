## Description:

Minimal local stock/crypto analysis with bundled Python scripts, public APIs, no credentials, and no subprocess calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run local stock, crypto, dividend, China-market, and portfolio analysis from public market data. The outputs support research workflows and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency verification claims and pinned requirement hashes may need review before installation.

Mitigation: Review requirements.txt, install in a fresh virtual environment, and do not bypass hash failures unless the packages are independently trusted.

Risk: Portfolio tracking stores financial holdings data locally.

Mitigation: Treat portfolios.json as private financial data and keep CLAWDBOT_STATE_DIR in a directory readable and writable only by the intended user.

Risk: Market analysis and recommendations can be incomplete, delayed, or misleading.

Mitigation: Use the results for informational research only and verify decisions against independent market data or qualified financial advice.

Risk: Public API queries expose ticker symbols and date ranges to external market-data providers.

Mitigation: Run the skill only in environments where those outbound public API requests are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/research-analyst)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands; bundled scripts print plain text or JSON analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portfolio commands may write local portfolio data to portfolios.json under the configured ClawHub state directory.]

## Skill Version(s):

1.0.54 (source: server release metadata; artifact frontmatter reports 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
