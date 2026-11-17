## Description:

Qinghu AI's Douyin Quick Listing skill helps agents source products from 1688, confirm Xiaofeng ERP authorization and templates, publish listings to Douyin shops, and edit listing titles, images, SKUs, and carousel images after listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and operations teams use this skill to move products from 1688 sourcing into Douyin shop listings through Qinghu and Xiaofeng ERP workflows. It is also used to inspect existing Douyin listings and apply user-approved title, image, SKU, shipping, purchase-limit, and carousel-image edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect live Douyin shop listings.

Mitigation: Confirm the target account, template, ordered link list, and requested edits before execution; use preview mode before final distribution when available.

Risk: Some data calls may consume Qinghu credits.

Mitigation: Obtain user approval before tool calls and report consumption from the returned pointCost value converted to Qinghu credits.

Risk: Wrong templates or unreviewed edits can require manual cleanup.

Mitigation: List available templates for user selection and submit only fields the user explicitly asked to change.

Risk: Exported or cached files may contain business records.

Mitigation: Treat exports as sensitive local files, provide concise previews, and avoid copying large datasets into chat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-douyin-quick-listing)
- [Qinghu data API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)
- [Xiaofeng ERP console](https://xfdyorder.zzbtool.com/zzb_super_goods_xf/index.html#/index)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, files]

**Output Format:** [Markdown status reports with JSON-RPC request examples and links to exported files when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account and template confirmations, listing success and failure counts, failure reasons, suggested next actions, and local export links for large result sets.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
