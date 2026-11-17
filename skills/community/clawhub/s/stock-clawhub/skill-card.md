## Description:

Stock Clawhub provides stock and ETF lookup guidance plus a Python query helper for price, detail, ETF, and recommendation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinewilzhang](https://clawhub.ai/user/shinewilzhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to ask an agent for stock and ETF lookup commands and basic query results. Prices, recommendations, and analysis should be treated as informational only and not used as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill overstates its analysis abilities compared with the included stock-query script.

Mitigation: Review the claimed capabilities against the artifact behavior before presenting analysis or recommendations to users.

Risk: The security review reports that financial queries are sent to an undocumented mock data service.

Mitigation: Do not rely on prices or recommendations for financial decisions unless provider disclosures, validation, and data provenance are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinewilzhang/skills/stock-clawhub)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text and JSON query results, with command examples in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries may call an undocumented mock stock data service; results require review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog lists v1.0.0 dated 2025-01-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
