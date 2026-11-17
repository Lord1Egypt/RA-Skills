## Description:

Fetches DiDi ride and hotel travel coupons and presents redemption links and QR code image links for use with WeChat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moooai](https://clawhub.ai/user/moooai)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and their assistants use this skill to find ride-hailing and hotel coupon offers and share links or QR codes for redemption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coupon links and QR codes lead to third-party redemption pages.

Mitigation: Check the destination and offer terms before opening, scanning, or sharing a coupon.

Risk: The helper script stores an anonymous installation identifier and sends it to the coupon API for attribution.

Mitigation: Privacy-sensitive users can avoid running the helper script or delete scripts/.install_id to rotate the identifier.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/moooai/skills/trip-coupon)
- [Publisher-listed project homepage](https://github.com/moooai/trip-coupon)
- [Coupon API documentation](references/api_documentation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text with coupon titles, redemption links, QR code image links, and instructions; optional JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coupon availability and links depend on the external coupon service; redemption is suggested through WeChat.]

## Skill Version(s):

2.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
