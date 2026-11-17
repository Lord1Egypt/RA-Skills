## Description:

Stock Selecter screens A-share stocks with configurable fundamental, technical, market-flow, and analyst-target strategies, supporting single-strategy and combined AND, OR, and SCORE ranking modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alan1121-j](https://clawhub.ai/user/alan1121-j)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen A-share equities with configurable strategy thresholds, combine strategy results, and review ranked outputs. Outputs should be treated as research support rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags insecure handling of a user API token and an HTTP API endpoint.

Mitigation: Review and fix the API endpoint before use, avoid sending tokens over HTTP, and rotate any Tushare token previously used with this release.

Risk: The security evidence flags misleading financial-strategy logic.

Mitigation: Treat generated rankings and reports as research inputs only, and independently review strategy logic before acting on results.

Risk: The skill can save JSON, CSV, and HTML outputs to a configured directory.

Mitigation: Control the output directory and review saved files before sharing or using them in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alan1121-j/skills/stock-selecter)
- [Tushare Pro registration](https://tushare.pro/register)
- [Tushare Pro documentation](https://tushare.pro/document/2)

## Skill Output:

**Output Type(s):** [text, JSON, CSV, HTML report, guidance]

**Output Format:** [JSON result object with optional CSV export and optional HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save timestamped screening outputs to a configured output directory.]

## Skill Version(s):

3.3.2 (source: ClawHub release evidence; artifact frontmatter and config report 3.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
