## Description:

青虎AI TikTok 达人带货建联：从达人库按站点和类目筛达人，批量查达人详情、达人视频列表与带货商品列表，反向从商品和店铺找关联带货达人，精准匹配高 ROI 达人，避免盲目寄样。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and commerce teams use this skill to find and assess TikTok Shop creators for product seeding and influencer outreach. It supports forward creator discovery by region and category, plus reverse lookup from competitor products or shops to identify creators with relevant sales history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Qinghu API key from the environment or from the user and makes authenticated external API calls after confirmation.

Mitigation: Install only when the Qinghu TikTok influencer data service is intended, confirm calls before use, and keep API keys scoped and out of shared outputs.

Risk: Large creator result sets may be exported to a local table file.

Mitigation: Treat exported files as local working data, share only necessary rows, and remove files that contain sensitive campaign or account information when no longer needed.

Risk: Creator recommendations can be misleading if API responses are incomplete, stale, or parsed incorrectly.

Mitigation: Check the documented success conditions, include region and period context in conclusions, and review recommended creators before outreach or product seeding.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-tiktok-influencer)
- [Qinghu MCP API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-RPC request examples and optional local table files for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creator recommendations are grouped by outreach priority and include reasons, performance context, content fit, and outreach suggestions.]

## Skill Version(s):

0.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
