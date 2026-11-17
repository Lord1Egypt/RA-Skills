## Description:

Trade Signal provides real-time Buy/Sell/Hold recommendations, price targets, technical analysis, and market-context answers for stocks, ETFs, options strategies, and global public securities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kslee9572](https://clawhub.ai/user/kslee9572)

### License/Terms of Use:


## Use Case:

External agents and users use this skill to request actionable market analysis, trade signals, target prices, technical levels, catalyst summaries, analyst-context summaries, and risk/reward commentary for public securities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that crafted query text can trigger local command execution through the shell wrapper.

Mitigation: Do not run the skill with untrusted query text until the query encoding bug is fixed; grant only narrow shell and network permissions.

Risk: The skill provides high-stakes trading signals and price targets that may be incorrect, incomplete, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as unverified informational signals rather than personalized financial advice, and require human review before acting on recommendations.

Risk: Queries may expose sensitive portfolio details to the remote trading-signal API.

Mitigation: Avoid sensitive portfolio, account, or personal financial details unless the deployment has explicit permission boundaries and data-handling approval.

## Reference(s):

- [Trade Signal ClawHub Page](https://clawhub.ai/kslee9572/skills/trade-signal-ttx)
- [Terminal X Homepage](https://terminal-x.ai)
- [Terminal X API Base](https://app.terminal-x.ai/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with markdown-formatted market analysis, citations, trade signals, price targets, and technical indicators.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The shell wrapper sends a user query to a remote API and returns the response without local post-processing.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
