## Description:

Turn a Shopify (or any e-commerce) product page URL into a 30-45 second 9:16 promo video ready for TikTok / Reels / Shorts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a public e-commerce product page into a short vertical promotional video with product imagery, captions, music, and generated video output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public product-page URLs and extracted product details are sent to Revid using REVID_API_KEY.

Mitigation: Use only public storefront URLs and avoid private, unpublished, customer-specific, or internal product pages unless sharing with Revid is approved.

Risk: Automatically scraped storefront pages may include irrelevant navigation, footer, review, or related-product content.

Mitigation: Keep or customize the scraping prompt to extract only the product name, hero image, key features, and price before rendering.

Risk: Generated captions, voice, music, or imagery may need brand or campaign review before publication.

Mitigation: Review the returned video and adjust voice, caption position, duration, or media settings before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/api00/skills/revid-shopify-product-promo)
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render)
- [Revid status API endpoint](https://www.revid.ai/api/public/v3/status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Revid render status details including pid, status, videoUrl, thumbnailUrl, durationSeconds, and creditsUsed when available.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
