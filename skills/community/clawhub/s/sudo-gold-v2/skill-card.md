## Description:

Sudo Gold helps agents retrieve gold market information and prepare price, technical, fundamental, and risk analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmouseboy](https://clawhub.ai/user/fmouseboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather current gold price, news, technical-indicator, and macro/fundamental signals and turn them into a concise market analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gold-market queries and the Tavily API key may be sent to an external search provider.

Mitigation: Disclose Tavily use before installation, require a user-controlled TAVILY_API_KEY, avoid sensitive queries, and rotate or revoke the key if exposure is suspected.

Risk: Generated gold analysis may be incomplete, stale, or mistaken and could be confused with investment advice.

Mitigation: Present outputs as informational analysis only, keep the risk disclaimer, review source results, and require users to make independent financial decisions.

Risk: The artifact includes an unrelated JD Finance promotional link that does not support the core analysis workflow.

Mitigation: Remove the promotional link or clearly treat it as advertising during release review.

## Reference(s):

- [Technical Indicators Reference](references/technical-indicators.md)
- [Sudo Gold ClawHub Release](https://clawhub.ai/fmouseboy/skills/sudo-gold-v2)
- [Tavily Search API Endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style analysis report with source listings and plain-text shell output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; live search results depend on Tavily responses.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
