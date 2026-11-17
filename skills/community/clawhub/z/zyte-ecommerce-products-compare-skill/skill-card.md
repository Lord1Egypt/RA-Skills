## Description:

Extracts structured product data from e-commerce URLs using the Zyte API and generates side-by-side comparison tables with purchase recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apscrapes](https://clawhub.ai/user/apscrapes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compare products from multiple e-commerce URLs, normalize prices, ratings, availability, and features, and receive a concise buying recommendation based on the user's stated intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Zyte API key and the documentation includes examples that place the key in environment or configuration values.

Mitigation: Use a dedicated Zyte API key with limited quota and keep real keys out of shared workspaces, logs, and committed configuration files.

Risk: The skill sends supplied product URLs to the Zyte API for extraction.

Mitigation: Use only public product pages and avoid authenticated, private, internal, or sensitive URLs.

Risk: Raw extraction responses are written to predictable /tmp paths by the bundled fetch script.

Mitigation: Run the skill only in a trusted local environment or revise the script to use per-run temporary directories and cleanup.

Risk: The troubleshooting documentation includes a command that rewrites /etc/resolv.conf.

Mitigation: Do not run that command; configure DNS through approved host or container settings instead.

Risk: Server security evidence marks the release as suspicious pending review.

Mitigation: Review and scan the skill before installation or deployment.

## Reference(s):

- [Zyte API](https://www.zyte.com/zyte-api/)
- [Zyte API Pricing](https://docs.zyte.com/zyte-api/pricing.html)
- [Zyte API Notes for Product Extraction](references/zyte-api-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/apscrapes/skills/zyte-ecommerce-products-compare-skill)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown comparison table and recommendation, with JSON summaries from bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include failed URL notes, currency mismatch notes, incomplete data notes, fetch timing, and parallel worker counts.]

## Skill Version(s):

1.0.0 (source: server evidence and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
