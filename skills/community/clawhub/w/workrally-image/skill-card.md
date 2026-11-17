## Description:

Paid image generation skill for text-to-image and image-to-image tasks, covering posters, illustrations, wallpapers, avatars, and logos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create static images from text prompts or reference images through WorkRally, with user confirmation and payment authorization before each generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional reference images are sent to WorkRally for processing.

Mitigation: Use the skill only when the user accepts WorkRally processing, and avoid sending sensitive reference images unless the user has approved that use.

Risk: Each generation is a paid action.

Mitigation: Show the 0.36 yuan per-call price and require explicit user confirmation and WeixinPay authorization before invoking generation.

Risk: Polling the content endpoint incorrectly could confuse unpaid, generating, failed, expired, or refunded states.

Mitigation: Use the same payment_id for content polling, follow returned status and retry_after_seconds values, and start a new invoke only for terminal failed or expired states.

## Reference(s):

- [Prompting Guide](references/prompting.md)
- [Pricing](references/pricing.md)
- [Invoke Flow](references/invoke-flow.md)
- [Troubleshooting](references/troubleshooting.md)
- [WorkRally Homepage](https://workrally.qq.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Files]

**Output Format:** [Markdown guidance with API request details and result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one 1K image result per paid generation and returns a WorkRally result URL when delivered.]

## Skill Version(s):

1.1.1 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
