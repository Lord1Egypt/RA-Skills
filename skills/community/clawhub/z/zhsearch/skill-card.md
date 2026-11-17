## Description:

Chinese search enhancement: search Baidu, Zhihu, and WeChat articles. Returns AI-optimized structured results in Chinese. Paid skill (0.001 USDT/call via SkillPay).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinp0830](https://clawhub.ai/user/jinp0830)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve Chinese-language search results from Baidu, Zhihu, and WeChat public account articles when general web search performs poorly for Chinese queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries leave the machine, including through an unlisted Baidu proxy.

Mitigation: Treat searches as non-private, avoid sensitive queries, and disclose all external endpoints before deployment.

Risk: Billing sends a stable local identifier to SkillPay while the skill documentation describes anonymous/no-local-files handling.

Mitigation: Update the privacy disclosure and review identity collection before production use.

Risk: The artifact includes a billing API key.

Mitigation: Rotate the exposed key and use a deployment pattern that does not distribute active billing secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinp0830/skills/zhsearch)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON search results grouped by source, with titles, snippets, URLs, and optional account/date fields; billing failures may return payment-required JSON with a payment_url.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be limited from 1 to 20 per selected source.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
