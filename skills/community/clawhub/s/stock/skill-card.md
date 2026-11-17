## Description:

Provides a CLI for querying real-time A-share and Hong Kong stock quote data from Sina Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrblackerx](https://clawhub.ai/user/mrblackerx)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to run stock quote lookups for supported A-share and Hong Kong symbols and receive concise market data in the agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried stock symbols are sent to Sina Finance.

Mitigation: Use the skill only when sending the requested symbols to Sina Finance is acceptable.

Risk: The documentation advertises US stock examples, but the inspected implementation supports A-share six-digit symbols and Hong Kong five-digit symbols only.

Mitigation: Treat the skill as suitable for A-share and Hong Kong lookups unless a future release adds verified US stock support.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrblackerx/skills/stock)
- [Publisher profile](https://clawhub.ai/user/mrblackerx)
- [Sina Finance](https://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text CLI output with stock name, symbol, price, price movement, daily range, volume, and market.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=14 and network access to Sina Finance; no credentials are required.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
