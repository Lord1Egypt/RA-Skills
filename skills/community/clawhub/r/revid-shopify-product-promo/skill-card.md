## Description: <br>
Turn a Shopify or other e-commerce product page URL into a 30-45 second vertical promo video for TikTok, Reels, or Shorts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, and developers use this skill to generate a short product promo video from a public storefront URL while letting Revid extract product details automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Revid receives the submitted public product page URL and extracted product details. <br>
Mitigation: Use only public storefront pages and avoid private, staging, authenticated, or unreleased product URLs. <br>
Risk: The skill requires a sensitive Revid API key. <br>
Mitigation: Store REVID_API_KEY securely and avoid exposing it in logs, prompts, shared scripts, or committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/api00/revid-shopify-product-promo) <br>
- [Example render payload](artifact/examples/shopify-aeropods.json) <br>
- [End-to-end curl example](artifact/examples/run.sh) <br>
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Revid render status details such as pid, videoUrl, thumbnailUrl, durationSeconds, and creditsUsed when the API call succeeds; requires REVID_API_KEY.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
