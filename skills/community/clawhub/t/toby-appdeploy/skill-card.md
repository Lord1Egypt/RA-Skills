## Description:

Deploy web apps with backend APIs, database, file storage, AI operations, authentication, realtime, and cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to deploy or update websites and web apps through SkillBoss API Hub and obtain a public URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends app files and deployment metadata to a third-party deployment API.

Mitigation: Use it only for repositories that do not contain secrets, private data, or credentials, and keep SKILLBOSS_API_KEY handling limited to the deployment call.

Risk: The skill asks the agent to follow live external deployment instructions before generating or deploying code.

Mitigation: Treat remote deployment instructions as service constraints, not permission to override the user's request, local policy, or security rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-appdeploy)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss API Hub deployment endpoint](https://api.skillboss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment status details and public app URLs returned by the deployment API.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
