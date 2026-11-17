## Description:

Retrieve complete TikTok Shop product details with the official Gecho Bridge MCP tool, including title, price, SKU, description, sales, ratings, and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, ecommerce teams, and developers use this skill to collect and summarize details for a single TikTok Shop product from a provided product URL or product ID. It is suited to product research workflows that rely on Gecho Bridge, the Gecho Chrome extension, and an active TikTok Shop browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a logged-in browser session and the Gecho Chrome extension to access TikTok Shop data.

Mitigation: Use it only after confirming trust in Gecho Bridge and the Chrome extension, and keep platform prompts such as login, region selection, and CAPTCHA under manual user control.

Risk: The setup examples use npx with an @latest package, which can change over time.

Mitigation: Pin or review the Gecho Bridge MCP package version in environments that require stricter supply-chain control.

Risk: Saved raw result files may contain product, store, or session-derived marketplace data.

Mitigation: Choose a trusted absolute save directory and review raw files before sharing them outside the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gecho-ai/skills/tiktok-product)
- [Gecho Website](https://gecho.ai/)
- [Gecho Bridge GitHub Repository](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw Setup Video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes Setup Video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Files]

**Output Format:** [Markdown guidance with inline shell command blocks and summarized structured product fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a local saved result path when the Gecho MCP tool saves raw product data; raw JSON is intentionally summarized rather than pasted in full.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
