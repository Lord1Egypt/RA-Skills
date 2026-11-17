## Description:

Instantly find the best AI agent skills, tools, and capabilities from across the entire web.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to search a publisher-operated global index for existing agent skills, tools, and prompts relevant to a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to a publisher-operated external API.

Mitigation: Do not include secrets, credentials, private project identifiers, customer data, or other sensitive information in search queries.

Risk: Search results are remote content and may be incorrect, stale, or unsuitable for the user's environment.

Mitigation: Review result origins and inspect any selected skill before installing, running, or relying on it.

## Reference(s):

- [Global Skills Search on ClawHub](https://clawhub.ai/h4gen/skills/skills-search-fts)
- [Publisher profile: h4gen](https://clawhub.ai/user/h4gen)
- [Search API endpoint](https://skillsearch-api.hagen-hoferichter.workers.dev/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text listing matching skills with names, origins, and descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and forwards search terms to an external publisher-operated search API.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
