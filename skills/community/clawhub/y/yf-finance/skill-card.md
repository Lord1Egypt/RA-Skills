## Description:

Fetch real-time and historical financial data from Yahoo Finance using yf-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erhwenkuo](https://clawhub.ai/user/erhwenkuo)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and external users use this skill to retrieve stock quotes, historical prices, company financials, earnings calendars, analyst data, options chains, dividends, market screeners, and financial news through yf-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run an unpinned third-party yf-cli package through uv.

Mitigation: Review and pin an approved yf-cli version before deployment, and run installation only in trusted environments.

Risk: Examples can redirect financial data output to files and may overwrite existing files.

Mitigation: Use explicit output filenames and check whether a target file already exists before redirecting command output.

Risk: Yahoo Finance data can be unavailable, delayed, rate limited, or reflect the last market close rather than a live price.

Mitigation: Retry once on transient failures, clearly label stale or last-close values, and avoid treating this output as investment advice.

## Reference(s):

- [yf-cli Command Reference](references/commands.md)
- [Output Formats](references/output-formats.md)
- [Worked Examples](assets/examples.md)
- [ClawHub skill page](https://clawhub.ai/erhwenkuo/skills/yf-finance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and yf-cli output that may be table, JSON, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.13+, uv, yf-cli, and internet access; JSON or CSV output can be used for downstream parsing.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
