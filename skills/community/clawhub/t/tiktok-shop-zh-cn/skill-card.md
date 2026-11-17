## Description:

通过官方 Gecho Bridge MCP 搜索 TikTok Shop 商品并获取已知商品详情。适用于商品发现、商品库调研、竞品比较、价格与销量信号分析，以及指定商品详情采集。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce operators use this skill to route TikTok Shop product discovery and product detail research through official Gecho Bridge MCP tools. It supports keyword search, candidate comparison, product detail collection, and concise summaries of prices, ratings, sales signals, variants, reviews, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a logged-in browser session and Chrome extension to read TikTok Shop pages visible to the user.

Mitigation: Install only if you trust Gecho Bridge and the extension, and consider using a dedicated browser profile for TikTok Shop research.

Risk: Saved product research JSON can contain account-visible or commercially sensitive product research data.

Mitigation: Provide save directories only where you are comfortable storing that data, and handle saved files according to your data policy.

Risk: TikTok Shop login walls, CAPTCHA prompts, unavailable products, or missing MCP tools can prevent reliable results.

Mitigation: Resolve browser prompts manually, verify Gecho MCP prerequisites before use, and stop rather than fabricating product data when tools fail or return incomplete results.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/gecho-ai/skills/tiktok-shop-zh-cn)
- [Gecho](https://gecho.ai/)
- [Gecho Bridge GitHub](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw TikTok Configuration Video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes TikTok Configuration Video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON files]

**Output Format:** [Markdown guidance with bash command blocks and optional saved JSON result paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes work through serial Gecho MCP calls and summarizes only data returned by the tools.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
