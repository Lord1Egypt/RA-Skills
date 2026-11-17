## Description:

通过官方 Gecho Bridge MCP 获取完整的 TikTok Shop 商品详情，包括标题、价格、SKU、描述、销量、评分和评价。用户提供 TikTok Shop 商品 URL 或商品 ID 时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce researchers use this skill to route TikTok Shop product URLs or product IDs to the official Gecho Bridge MCP workflow, collect product-detail fields, and summarize the most useful results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a logged-in Chrome session, the Gecho Chrome extension, and TikTok Shop access, so missing login, verification, region, or cookie steps can block collection.

Mitigation: Before running the workflow, confirm Gecho and TikTok Shop are logged in through Chrome and manually resolve verification, region, and cookie prompts.

Risk: The MCP tool can write result files when a save directory is supplied.

Mitigation: Provide a save directory only when local result files are desired, and use a directory with appropriate write permissions.

Risk: Using unofficial scraping or browser automation outside the Gecho workflow could change the operational and compliance risk profile.

Mitigation: Use only the official Gecho Bridge MCP `tiktok_product` workflow for this skill and stop on tool errors or empty results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/tiktok-product-zh-cn)
- [Gecho Bridge](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho website](https://gecho.ai/)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference saved local result paths when the Gecho MCP workflow returns them; avoids pasting full raw JSON into the chat.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
