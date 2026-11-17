## Description:

Provides cloud-backed cross-border ecommerce SEO keyword research and structured placement reports for Amazon, Shopify, and TikTok Shop from user-supplied product, seed keyword, competitor keyword, market, and language inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, marketers, and agent workflows use this skill to generate keyword expansion and SEO placement reports for Amazon, Shopify, and TikTok Shop listings. The reports help plan title, bullet, backend keyword, meta, collection tag, hashtag, and video hook usage before human review and platform publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TOKENAPI_BASE_URL can redirect the bearer token and business inputs to an endpoint outside the expected Yufluent service.

Mitigation: Keep TOKENAPI_BASE_URL unset for normal use, or set it only to a trusted HTTPS Yufluent endpoint or a local development server.

Risk: TOKENAPI_KEY grants access to a cloud service and may expose account value if leaked.

Mitigation: Store TOKENAPI_KEY as a secret, avoid committing it, and rotate it if it is exposed.

Risk: SEO reports are generated from supplied inputs and cloud service rules, not live marketplace ranking or search-volume APIs.

Mitigation: Review recommendations against seller analytics, advertising search terms, platform policies, and product facts before publishing listing content.

Risk: Competitive keywords and product strategy are sent to a third-party cloud service.

Mitigation: Avoid submitting highly sensitive competitive data unless the Yufluent service terms and internal data handling requirements are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluent-clawhub-publish-yufluentcn-seo-pro)
- [Yufluent service homepage](https://claw.changzhiai.com)
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON report or formatted text printed by the CLI, with optional JSON file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY and the requests dependency; TOKENAPI_BASE_URL is optional and should point only to a trusted endpoint.]

## Skill Version(s):

1.1.2 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
