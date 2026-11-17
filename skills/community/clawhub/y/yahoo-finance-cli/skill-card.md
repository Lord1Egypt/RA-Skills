## Description:

This skill should be used when the user asks to "get stock prices", "check stock quotes", "look up earnings", "get financial data", "find trending stocks", or needs stock market data from Yahoo Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stuhorsman](https://clawhub.ai/user/stuhorsman)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to retrieve Yahoo Finance market data, including stock quotes, earnings data, fundamentals, analyst recommendations, symbol search results, trending symbols, and historical price data through a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow can persistently modify a system-wide command path.

Mitigation: Prefer a user-local or project-local install, and avoid sudo or forced /usr/local/bin symlinks unless the target binary and any existing yf command have been verified.

Risk: The npm dependency is unpinned.

Mitigation: Pin and audit yahoo-finance2 before using the skill in managed or production environments.

Risk: The Yahoo Finance CLI may store cookies in ~/.yf2-cookies.json.

Mitigation: Review local cookie handling expectations and remove the cookie file when troubleshooting or when local retention is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stuhorsman/skills/yahoo-finance-cli)
- [Publisher profile](https://clawhub.ai/user/stuhorsman)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced Yahoo Finance CLI outputs JSON that can be filtered with jq.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
