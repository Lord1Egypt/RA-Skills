## Description:

Search TikTok Shop products and retrieve known product details through the official Gecho Bridge MCP tools. Use for product discovery, catalog research, competitor comparison, pricing, sales signals, and item-level detail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and ecommerce researchers use this skill to search TikTok Shop products, compare listings, inspect known product details, and summarize pricing, ratings, sales signals, variants, reviews, and links returned by the official Gecho Bridge MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Gecho's Chrome extension and MCP server operating against a logged-in TikTok Shop browser session.

Mitigation: Install it only when that browser-session access is acceptable, keep the extension logged in intentionally, and resolve login walls, CAPTCHA, verification prompts, or blocked pages manually before retrying.

Risk: Product research output can be incomplete when TikTok Shop listings are unavailable, private, deleted, blocked, or not returned by the official tools.

Mitigation: Report the exact page or tool state and avoid inventing prices, sales, ratings, reviews, links, or product details that were not returned.

Risk: Running multiple scraping jobs at once can conflict with the single live browser tab and extension session required by the workflow.

Mitigation: Run Gecho jobs sequentially and use only one product discovery or product-detail MCP call in a conversational turn.

## Reference(s):

- [Gecho website](https://gecho.ai/)
- [Gecho Bridge GitHub repository](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw setup video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes setup video](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/tiktok-shop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise summaries, setup commands, troubleshooting guidance, and optional local JSON result paths from the MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes returned TikTok Shop product listings or product details without inventing missing data; raw results may be saved locally when the official tool reports a path.]

## Skill Version(s):

1.1.38 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
