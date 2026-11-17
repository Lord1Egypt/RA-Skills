## Description:

Автоматический поиск клиентов (родителей) для репетитора по математике в группах ВКонтакте с умной фильтрацией и приоритизацией онлайн-запросов.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danil4091](https://clawhub.ai/user/danil4091)

### License/Terms of Use:


## Use Case:

External math tutors use this skill to monitor configured VK groups for parent requests, filter out tutor advertising, prioritize online tutoring leads, and produce a short scan report with saved lead records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a VK service token in plaintext configuration.

Mitigation: Use a least-privilege token, do not commit or share filled configuration files, and rotate the token if it is exposed.

Risk: Recurring VK monitoring can build a local lead database from public social-media posts.

Mitigation: Confirm the collection is appropriate for the intended use, keep only necessary records, delete CSV or Sheet data when no longer needed, and ensure the three-hour schedule can be disabled.

Risk: The security review flags insufficient controls and privacy guidance for repeated social-media data collection.

Mitigation: Review the workflow and privacy expectations before deployment and add operational controls for retention, access, and opt-out handling where applicable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danil4091/skills/vk-client-search-repetitor)
- [VK Developers app management](https://vk.com/apps?act=manage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, Files]

**Output Format:** [Markdown report plus CSV lead records and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured VK service token, target VK group list, recurring three-hour checks, keyword filtering, deduplication, and priority labels.]

## Skill Version(s):

1.0.0 (source: frontmatter, config.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
