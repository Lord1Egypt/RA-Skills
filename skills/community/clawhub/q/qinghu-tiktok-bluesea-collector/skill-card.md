## Description:

Qinghu AI's TikTok Blue Ocean Product Collector helps agents find emerging TikTok Shop products, inspect product details, source matching items on 1688, and estimate gross margin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and sourcing analysts use this skill to identify rising TikTok Shop products, compare product details, find matching 1688 suppliers, and produce prioritized candidates with margin assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require a Qinghu API token for external product research calls.

Mitigation: Request the token only from the user or approved environment variables, send it only to the disclosed Qinghu endpoint, and avoid exposing it in outputs.

Risk: Qinghu API calls may consume account credits.

Mitigation: Obtain user approval before calls that may consume credits and report actual consumption using the returned pointCost conversion.

Risk: Exported spreadsheets or cached files may contain product research data.

Mitigation: Treat exported and cached files as user data and share only the intended file links or concise previews.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-tiktok-bluesea-collector)
- [Qinghu MCP API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API keys dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Concise Markdown summaries with optional spreadsheet or table exports and links to cached result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include blue-ocean candidate lists, supplier links, purchase prices, minimum order quantities, supplier qualifications, margin estimates, assumptions, and priority rationale.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
