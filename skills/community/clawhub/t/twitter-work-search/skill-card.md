## Description:

Searches X(Twitter) by keyword across top, latest, media, people, and list modes, then returns structured results with post text, engagement metrics, media details, and author information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, marketing teams, brand owners, and content creators use this skill to search X(Twitter) for topic tracking, market research, sentiment monitoring, competitor analysis, and content discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends X(Twitter) search terms and pagination requests to redfox.hk.

Mitigation: Use it only when sharing those search terms with RedFox is acceptable, and avoid submitting sensitive or confidential queries.

Risk: The skill requires a RedFox API key.

Mitigation: Store the API key in the supported environment variable or configuration file and rotate it if exposure is suspected.

Risk: Short follow-up requests such as "continue" may load another page from the previous search.

Mitigation: Confirm the active search context before using pagination language in multi-topic conversations.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/redfox-data/redfox-community/tree/main/skills/twitter-work-search)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/twitter-work-search)
- [Core workflow](references/core_workflow.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 20 results per page with optional pagination prompts; includes post text, links, engagement counts, media indicators, and author details when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
