## Description:

Queries Vipshop product details by product ID or product link and returns structured product information including pricing, discounts, images, reviews, brand information, and product links after Vipshop login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vip](https://clawhub.ai/user/vip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to look up Vipshop product details from a product ID or link and present a concise shopping summary with product images, prices, discounts, service tags, authenticity information, reviews, and a product link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated product links may include exchange-token data that can expose Vipshop account access if shared or displayed.

Mitigation: Do not publish or forward generated product links that contain exchange-token parameters; prefer ordinary product detail links and refresh or revoke the Vipshop login session if such links were shared.

Risk: The skill automatically reads stored Vipshop login tokens and may trigger or install a login dependency.

Mitigation: Require explicit user approval before installing or invoking login flows, and verify the dependency identity before use.

Risk: The skill depends on Vipshop network APIs and a valid login state, so results may fail or be incomplete when tokens expire or auxiliary endpoints are unavailable.

Mitigation: Handle token-expired and endpoint-failure responses clearly, reauthenticate through a verified login flow, and fall back to main product information when auxiliary data is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vip/skills/vip-product-detail)
- [Vipshop product detail API endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/detail/main/v6)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown product summary backed by JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Vipshop login state and network access; auxiliary product detail data may be unavailable and the skill can fall back to main product information.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
