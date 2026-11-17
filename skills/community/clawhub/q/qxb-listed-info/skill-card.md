## Description:

Queries cross-market listed-company information for A-shares, NEEQ, and H-shares, including basic listing data, shareholder details, and latest financial indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llx-26](https://clawhub.ai/user/llx-26)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to retrieve standardized public listing, shareholder, market-value, and financial-report data for Chinese listed enterprises by company name or enterprise ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends QXBENT_API_TOKEN as a persistent credential to Qixin's listed-company API.

Mitigation: Protect the token as a secret, avoid logging it, and rotate it if it may have been exposed.

Risk: Company-name lookup can resolve to an unintended enterprise when names are ambiguous or fuzzy matched.

Mitigation: Verify the returned enterprise name before relying on results, and use eid for important work.

Risk: Runtime dependency behavior may change when installing unpinned compatible dependency ranges.

Mitigation: Pin and review dependencies for production installations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llx-26/skills/qxb-listed-info)
- [getListedInfo API reference](references/getListedInfo.md)
- [Qixin API token center](https://www.qixin.com/app-center/home?route=skill-quota)
- [Qixin listed-company API base](https://external-api.qixin.com/skill/ent/public)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with TypeScript examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return listing arrays containing market data, shareholder records, and financial report fields from Qixin.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
