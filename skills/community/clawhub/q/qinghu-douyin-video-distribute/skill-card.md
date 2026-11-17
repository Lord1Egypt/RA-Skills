## Description:

青虎AI 抖音爆款视频跟卖与铺货 helps agents discover rising Douyin commerce videos, collect matching 1688 sources, and prepare confirmed Xiaofeng ERP distribution to Douyin shops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and agents use this skill to identify Douyin videos with fast sales momentum, find same-item supply on 1688, and prepare reviewed listing distribution through Xiaofeng ERP for Douyin shops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Qinghu credentials and may consume paid Qinghu credits during data calls.

Mitigation: Confirm the Qinghu token or account before use, obtain authorization before tool calls, and report actual credit consumption from the response envelope.

Risk: Exported video, supplier, or listing files may contain sensitive business data.

Mitigation: Review exported files before sharing them and keep exports in approved storage locations.

Risk: ERP distribution can create or move live Douyin shop listings if execution parameters are approved incorrectly.

Mitigation: Confirm account, template, link order, and listing parameters before live distribution; use preview mode before execution when available.

Risk: Following third-party popular products or videos can create brand, patent, or content-rights exposure.

Mitigation: Require the user to review brand authorization, patent concerns, and video material rights before sourcing or listing similar products.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-douyin-video-distribute)
- [Publisher profile](https://clawhub.ai/user/autoagc)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys)
- [Xiaofeng ERP backend](https://xfdyorder.zzbtool.com/zzb_super_goods_xf/index.html#/index)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, files, guidance]

**Output Format:** [Markdown summaries with structured lists, JSON examples, API call guidance, and exported spreadsheet files when record volume warrants it]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports video candidates, matching 1688 sources, ERP account/template choices, listing results, failure reasons, and Qinghu credit consumption when paid calls are made.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
