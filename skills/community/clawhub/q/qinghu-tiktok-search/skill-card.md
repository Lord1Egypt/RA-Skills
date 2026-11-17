## Description:

Searches TikTok for creators, products, shops, videos, and live streams by keyword, with up to 30 results per search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers, marketers, and researchers use this skill to find TikTok creators, products, shops, videos, live streams, and category IDs for a search term.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading runtime packages, especially unpinned versions, can change the local environment.

Mitigation: Review the dependency and install or update it yourself where possible; avoid unpinned packages in privileged environments.

Risk: Persisting an API token can expose account access if the environment is not trusted.

Mitigation: Configure the token yourself in a trusted environment and review how credentials are stored.

Risk: Search calls can incur Qinghu credits, and costs vary with the number of results.

Mitigation: Check the current estimate and obtain user approval before any paid call.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-search)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise answers with key results; a table file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 30 records per search; report actual credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
