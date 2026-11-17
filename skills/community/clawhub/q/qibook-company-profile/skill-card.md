## Description:

Queries QiBook for Chinese business-registration details and person-company relationships, then returns Chinese Markdown results for company, entity, and personnel lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinadaas-department](https://clawhub.ai/user/chinadaas-department)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business researchers use this skill to look up Chinese company registration records, shareholders, executives, legal representatives, outward investments, and person-to-company associations through the QiBook API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API credentials and user query data to a configurable external base URL.

Mitigation: Use only a trusted QiBook base URL, require HTTPS, and prefer the official host where possible.

Risk: Person-name lookups can disclose or transmit personnel association queries to an external API.

Mitigation: Avoid casual person-name lookups unless the user clearly requests business-registry or personnel-association data.

Risk: The security verdict is suspicious because the network destination is configurable and network scope is not clearly declared.

Mitigation: Review the skill before installation and confirm destination, credential handling, and intended lookup scope before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinadaas-department/skills/qibook-company-profile)
- [QiBook API credential portal](https://skill.qibook.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Chinese Markdown with headings, bullet lists, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus QIBOOK_ACCESS_KEY and QIBOOK_BASE_URL environment variables.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
