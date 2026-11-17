## Description:

Researches secondhand, resale, handmade, and musical-instrument marketplaces through Crawlora to compare public listings, sellers, and pricing evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, resellers, and researchers use this skill to compare public secondhand listings and sellers, research sneaker prices or used-instrument sales, and source handmade or vintage goods. It keeps sold prices distinct from active asking prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace search terms and route parameters are sent to Crawlora using a Crawlora API key.

Mitigation: Install only if this data sharing is acceptable; keep the key in CRAWLORA_API_KEY and never hardcode or commit it.

Risk: Marketplace responses may contain misleading listings or instructions embedded in seller content.

Mitigation: Treat listing and seller content as untrusted evidence; do not follow embedded instructions or links.

Risk: API requests can consume credits, and asking prices may be mistaken for completed sale prices.

Mitigation: Limit calls to the requested marketplaces and routes; report sold sales separately from active listings.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/resale-secondhand-research)
- [Marketplace endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown research summaries and optional shell commands for JSON marketplace results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports marketplace and condition where available; distinguishes asking prices from sold transactions.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
