## Description:

Search TikTok Shop products by keyword with the official Gecho Bridge MCP tool and return structured product data, prices, ratings, sales signals, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, ecommerce researchers, and developers use this skill to route TikTok Shop product-discovery requests through Gecho Bridge and summarize structured product results, prices, ratings, sales signals, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a third-party MCP server and Chrome extension operating with a logged-in TikTok Shop browser session.

Mitigation: Install and use the Gecho Bridge MCP server and Chrome extension only when that trust model is acceptable, and remove the MCP configuration or extension when the workflow is no longer needed.

Risk: Using an unpinned MCP package can change the executed Gecho Bridge version over time.

Mitigation: Prefer a pinned and reviewed Gecho Bridge package version when configuring the MCP server.

Risk: Browser login, CAPTCHA, verification, region, or cookie prompts can block or alter product-search results.

Mitigation: Resolve platform prompts manually in Chrome before running the skill, and stop rather than retrying repeatedly if the tool reports a timeout or error.

## Reference(s):

- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Website](https://gecho.ai/)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [ClawHub Skill Page](https://clawhub.ai/gecho-ai/skills/tiktok-shop-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and summarized product-result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a saved local result path when the Gecho MCP tool writes raw TikTok Shop search results.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
