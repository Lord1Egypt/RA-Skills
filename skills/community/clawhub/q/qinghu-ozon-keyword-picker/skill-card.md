## Description:

Helps agents analyze Ozon keyword demand using Qinghu data APIs, including hot keyword rankings, keyword detail and trend snapshots, keyword-linked products, and product traffic keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce analysts, and agent operators use this skill to evaluate Ozon search demand, compare keyword opportunities, trace what products receive traffic from target keywords, and turn the analysis into selection and listing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Qinghu data APIs that require a user-provided token and may charge Qinghu credits.

Mitigation: Ask for deliberate user confirmation before API calls, use the configured Qinghu token only for the disclosed endpoint, and report actual costs from returned pointCost values.

Risk: Large Ozon keyword or product result sets may be exported to local spreadsheet files or links.

Mitigation: Tell the user when data is exported, keep chat previews concise, and avoid copying full cached datasets into the conversation.

Risk: Keyword demand conclusions can be misleading if data from different sites, periods, or update windows is compared directly.

Mitigation: Label metrics with site, accounting period, ranking period, and sample size, and avoid mixing incompatible periods in one comparison.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-ozon-keyword-picker)
- [Qinghu MCP API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu login](https://www.iqinghu.com/workbench/login?type=1&urlCode=1788417429126)
- [Qinghu API keys dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown summaries with keyword lists, product opportunity guidance, concise previews, and exported spreadsheet files or links for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Qinghu token; API calls should be confirmed before use and costs should be reported from returned pointCost values.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
