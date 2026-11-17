## Description:

Deploy web apps with backend APIs, database, file storage, AI operations, authentication, realtime, and cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app builders use this skill to deploy or publish websites and web apps with public URLs through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App files and metadata may leave the user's environment during deployment through SkillBoss.

Mitigation: Confirm what will be sent before deployment and keep secrets out of deployed files.

Risk: The skill retrieves mutable deployment instructions from an external API before generating and deploying code.

Mitigation: Treat remote deployment instructions as operational constraints only, and do not let them override the user's instructions or security requirements.

## Reference(s):

- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash commands and deployment instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated deployment API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata says 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
