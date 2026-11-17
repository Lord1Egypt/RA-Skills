## Description:

Searches products across Taobao, JD, Pinduoduo, Amazon, and other marketplaces, then generates affiliate links using the user's configured referral IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mi426878](https://clawhub.ai/user/mi426878)

### License/Terms of Use:

MIT-0

## Use Case:

External users and affiliate publishers use this skill to configure marketplace referral IDs, search products, compare results, and produce shareable affiliate links. Review search output before using it for purchase recommendations because the security evidence says current product prices and sales data are demo data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results may present demo prices and sales data as if they were live marketplace information.

Mitigation: Treat search output as demonstration data unless the skill is changed to call real marketplace APIs, and verify products directly before making or sharing purchase recommendations.

Risk: Generated links include affiliate identifiers that may require disclosure and platform-policy compliance.

Mitigation: Disclose affiliate relationships when sharing links and follow the promotion rules for each marketplace.

Risk: Affiliate IDs are stored locally in the skill directory.

Mitigation: Avoid committing local configuration files and restrict access to the skill directory when referral IDs are configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mi426878/skills/shopping-affiliate-search)
- [Publisher profile](https://clawhub.ai/user/mi426878)
- [Alimama affiliate platform](https://pub.alimama.com)
- [JD Union](https://union.jd.com)
- [Pinduoduo affiliate platform](https://jinbao.pinduoduo.com)
- [Amazon Associates](https://affiliate-program.amazon.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with affiliate search results, referral links, configuration examples, and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local affiliate configuration under the skill directory when referral IDs are configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
