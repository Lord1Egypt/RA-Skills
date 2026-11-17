## Description:

This skill helps agents research Douyin blue-ocean product opportunities by combining trend and video demand signals with 1688 sourcing checks through Qinghu APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and commerce researchers use this skill to identify niche Douyin product scenarios, validate content demand, locate 1688 supply, estimate gross margin, and prioritize candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Qinghu API token.

Mitigation: Use a purpose-scoped token where possible and avoid sharing the token beyond the agent environment that needs Qinghu API access.

Risk: API calls may consume Qinghu credits.

Mitigation: Confirm intended Qinghu tool use before calls and report consumed Qinghu credits from the response envelope.

Risk: Trend and sourcing data can support product hypotheses but may not prove demand, quality, or profitability.

Mitigation: Cross-check Douyin content signals with 1688 supply details, state pricing assumptions, and validate supplier quality before acting.

Risk: Large result sets may be exported to table files.

Mitigation: Review exported files before sharing and keep only the data needed for the product-research task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-douyin-bluesea-collector)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API keys dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown summaries with optional exported table files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions for numeric estimates and may include concise previews with file links for larger datasets.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
