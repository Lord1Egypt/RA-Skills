## Description:

Helps agents research localized search results, autocomplete ideas, and Google Trends through the Crawlora API without treating those signals as universal keyword volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners and developers use this skill to collect search-result snapshots, discover suggested queries, and compare regional or temporal search trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, locale parameters, and the Crawlora API key are sent to Crawlora.

Mitigation: Use only when that external transmission is acceptable; avoid confidential investigations and personal data, and keep the API key out of shared files.

Risk: Documented Google web search examples may fail because of an endpoint allowlist mismatch.

Mitigation: Verify Google search availability before relying on it, and use another suitable engine when needed.

## Reference(s):

- [Crawlora search and trend endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [SERP Keyword Research on ClawHub](https://clawhub.ai/crawlora-org/skills/serp-keyword-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Search and trend results in JSON, with agent summaries or shell examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect provider-specific snapshots; autocomplete and trend signals are not keyword-volume estimates.]

## Skill Version(s):

1.0.23 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
