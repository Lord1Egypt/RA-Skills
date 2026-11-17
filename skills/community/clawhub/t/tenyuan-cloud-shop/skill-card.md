## Description:

TenYuan Cloud Shop turns a product description or product photos into a shareable cloud shop page with product imagery, voiceover audio, share text, and seller contact details while keeping transactions offline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyruan](https://clawhub.ai/user/johnnyruan)

### License/Terms of Use:

MIT

## Use Case:

External sellers and small merchants use this skill to create a lightweight product storefront they can share on WeChat, social feeds, or with customers. The skill is for display and lead generation; sales, payment, fulfillment, and disputes remain offline between seller and buyer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product descriptions, images, phone numbers, WeChat IDs, and QR-code contact details may be uploaded to ruancyai.com and published on shareable pages.

Mitigation: Tell users the storefront is public-facing and avoid uploading sensitive personal, payment, or business information unless it is intended for publication.

Risk: Creating a shop page is a paid cloud action with a disclosed ¥9.9 charge.

Mitigation: Confirm the charge before creating a shop page and use the documented free endpoints for QR-code upload, share materials, and payment status checks where appropriate.

Risk: AI-generated images, names, slogans, and voiceover copy can misrepresent product facts or imply unsupported claims.

Mitigation: Clearly label AI-generated images as illustrative, keep prices and claims grounded in the seller's input, and avoid unsupported health or efficacy claims.

Risk: The hosted backend may be unavailable or not fully deployed, which could make shop creation fail.

Mitigation: When the service is unreachable or returns configuration errors, report that the cloud shop service is unavailable instead of fabricating links or shop data.

## Reference(s):

- [Backend API Contract](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/johnnyruan/skills/tenyuan-cloud-shop)
- [Hosted Cloud Shop Service](https://ruancyai.com/cloud)

## Skill Output:

**Output Type(s):** [text, markdown, api_calls, guidance]

**Output Format:** [Markdown or plain text containing a hosted shop URL, share copy, generated shop details, and optional voiceover audio URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creating a shop page is a paid cloud action at ¥9.9 per successful shop; QR-code upload, share material retrieval, and payment status checks are documented as free.]

## Skill Version(s):

0.3.2 (source: frontmatter and changelog, released 2026-08-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
