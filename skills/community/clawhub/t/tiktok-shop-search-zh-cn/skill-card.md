## Description:

通过官方 Gecho Bridge MCP 按关键词搜索 TikTok Shop 商品，返回商品数据、价格、评分、销量信号和链接。用户需要 TikTok Shop 商品发现或竞品商品调研时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, ecommerce operators, and product researchers use this skill to route TikTok Shop product-search requests through Gecho Bridge and summarize useful product data, prices, ratings, sales signals, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The working setup requires trusting Gecho's Chrome extension and MCP package while connected to a logged-in TikTok Shop browser session.

Mitigation: Use the skill only for product research appropriate for that integration, and review the external Gecho package or extension when strict data-handling requirements apply.

Risk: Login, verification, region, cookie, or browser-session prompts can block or reduce product-search results.

Mitigation: Resolve platform prompts manually in Chrome before retrying, and do not attempt to bypass verification.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/gecho-ai/skills/tiktok-shop-search-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional shell command blocks and summarized product data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes selected TikTok Shop product-search results and may report a saved results path when the Gecho MCP tool succeeds.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
