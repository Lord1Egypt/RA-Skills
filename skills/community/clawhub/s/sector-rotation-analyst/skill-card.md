## Description:

Identify sector rotation opportunities across all 11 GICS sectors using relative strength, momentum, and macro regime context from the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare sector leadership, infer sector rotation signals, and produce tactical overweight, neutral, and underweight recommendations from Finskills market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad or overprivileged Finskills API key could expose more access than the skill needs.

Mitigation: Use a Finskills API key with only the permissions needed for the requested market data.

Risk: Prompts may include confidential portfolio, strategy, or account information when asking for sector analysis.

Mitigation: Avoid including confidential portfolio, strategy, or account details in prompts that may lead to API lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/sector-rotation-analyst)
- [Publisher profile](https://clawhub.ai/user/finskills)
- [Homepage](https://github.com/finskills/sector-rotation-analyst)
- [Finskills API](https://finskills.net)
- [Finskills registration](https://finskills.net/register)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown sector rotation report with ranked tables and tactical recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY for Finskills API-backed market data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
