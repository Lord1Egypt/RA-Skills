## Description:

This unofficial MCP-style skill lets agents query Vietnam stock market data, including real-time and historical prices, company financials, market statistics, fund information, gold prices, and exchange rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to let an agent retrieve and summarize Vietnam market data for equities, company disclosures, funds, gold prices, and exchange rates through the XiaoBenYang API. It is suited to market research and data lookup workflows where the user can provide the required API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a limited or revocable key, keep the workspace private, and do not commit the .env file.

Risk: The security evidence marks the release suspicious because stale gaokao references remain in a Vietnam stock-data skill.

Mitigation: Review the skill before installation and ask the publisher for a cleaned-up release when provenance or behavior must be clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/vnstock)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON-like API results summarized as human-facing text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls return success status, raw upstream data, and a message; output_format options include json, dataframe, and toon, with toon as the default agent-optimized format.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
