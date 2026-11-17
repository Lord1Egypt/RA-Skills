## Description:

Research TikTok ads alongside TikTok Shop products and stores using PipiAds ad and TikTok Shop analytics tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research TikTok ad creatives, TikTok Shop products, and TikTok Shop stores together. It helps compare creative patterns with product momentum, GMV, sales, pricing, and store positioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a globally installed third-party PipiAds MCP server and access to a PipiAds API key.

Mitigation: Install only if the PipiAds MCP package is trusted, use a dedicated or limited API key where possible, and prefer an isolated environment when handling sensitive local data.

Risk: Broad search and detail workflows can consume PipiAds account credits.

Mitigation: Ask for category, region, price band, and time window before broad TikTok Shop research, and monitor credit and billing usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/tiktok-shop-ad-library-analytics)
- [PipiAds homepage](https://www.pipiads.com)
- [PipiSpy API key and billing](https://www.pipispy.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls, configuration]

**Output Format:** [Markdown or text summaries with tool-call guidance and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm and a PIPIADS_API_KEY for the PipiAds MCP server; API calls may consume PipiAds account credits.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
