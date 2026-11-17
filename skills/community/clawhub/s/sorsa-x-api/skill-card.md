## Description:

Retrieves public X/Twitter profiles, posts, search results, and related data through the Sorsa API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keksich13](https://clawhub.ai/user/keksich13)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to retrieve and review public X/Twitter data, including profiles, posts, search results, and account relationships. It also supports crypto-focused influence analysis using Sorsa Score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are received by Sorsa, and API use may incur charges.

Mitigation: Use a dedicated Sorsa API key and set page limits to control request volume.

Risk: The requests dependency may change within its allowed version range.

Mitigation: Review dependency versions before installing or deploying.

## Reference(s):

- [API reference](references/api-reference.md)
- [Sorsa API documentation](https://docs.sorsa.io/)
- [Sorsa API overview and key dashboard](https://api.sorsa.io/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Code, Shell commands]

**Output Format:** [Text or Markdown summaries, with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public X/Twitter data; requires a Sorsa API key.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
