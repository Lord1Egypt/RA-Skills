## Description:

青虎AI TikTok 单品分析 helps users evaluate TikTok Shop product details, channel dependence, creator/video/live performance, comments, stocking, and promotion budget using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, product analysts, and agents use this skill to assess a known TikTok Shop product's sales strength, traffic channel mix, review sentiment, stocking decision, and promotion budget allocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product queries and the Qinghu bearer token are sent to iqinghu.com.

Mitigation: Install only when intending to use Qinghu's TikTok product-analysis API, use a user-provided Qinghu token or approved environment variable, and avoid exposing the token in responses or exported files.

Risk: Qinghu API calls may consume Qinghu credits.

Mitigation: Get user confirmation before API calls, use the returned pointCost as the authoritative charge signal, and report the converted Qinghu credit total when paid calls occur.

Risk: Large result sets may be exported to local files.

Mitigation: Share export links intentionally, keep chat previews concise, and review exported data before broader distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-tiktok-product-analyst)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu login](https://www.iqinghu.com/workbench/login?type=1&urlCode=1788417429126)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown response with concise analysis and optional exported spreadsheet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before Qinghu API calls; larger record sets are exported instead of pasted into chat.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
