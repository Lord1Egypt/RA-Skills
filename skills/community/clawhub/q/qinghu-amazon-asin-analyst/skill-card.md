## Description:

Analyzes a specified Amazon ASIN or product link with Qinghu data to summarize product status, price and BSR history, Buy Box and seller changes, review trends, variant relationships, FBA cost details, traffic keywords, and conversion keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, ecommerce operators, and agents use this skill to inspect a known ASIN for competitor analysis, pricing decisions, listing diagnostics, and follow-seller risk assessment. It produces conclusion-first product research based on Qinghu ASIN, Keepa-style trend, review, traffic keyword, order keyword, and competitor data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASINs, Amazon links, and the Qinghu API token are used with the Qinghu service.

Mitigation: Install only for intended Qinghu Amazon product research, provide credentials deliberately, and review the first authorization prompt before approving data calls.

Risk: Paid Qinghu data calls may consume Qinghu points.

Mitigation: Require user approval before calls, use the returned pointCost as the source of truth, and report consumption separately after paid calls.

Risk: Large result sets may be exported to local files.

Mitigation: Treat exported product research files as local sensitive working data and share them only with intended recipients.

Risk: HTTP 200 responses or low-level success flags can still contain failed business responses.

Mitigation: Check protocol errors, result.isError, and the parsed inner JSON code and success fields before treating a call as successful.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-amazon-asin-analyst)
- [Qinghu MCP API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API keys dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)
- [Qinghu workflow authentication check endpoint](https://www.iqinghu.com/api/desktop/qh/workflow/page?pageNum=1&pageSize=5)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Conclusion-first Markdown product analysis with JSON API-call examples and optional exported table files for larger result sets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request a Qinghu API token, asks for approval before Qinghu data calls, and reports Qinghu point consumption when paid calls occur.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
