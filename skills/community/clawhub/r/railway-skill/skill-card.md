## Description:

Deploy and manage applications on Railway.app. Use for deploying projects, managing services, viewing logs, setting environment variables, and managing databases. Railway is a modern cloud platform for deploying apps with zero configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leicao-me](https://clawhub.ai/user/leicao-me)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to ask an agent for Railway CLI guidance for deploying projects, managing services, reading logs, configuring variables, and provisioning databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Railway deploys, deletes, database commands, and secret reads can affect real projects and production data.

Mitigation: Require explicit confirmation before production deploys, deletion, database operations, or secret reads; prefer staging and read-only database access where possible.

Risk: Environment-variable output may expose secrets.

Mitigation: Redact environment-variable values before sharing logs or agent output, and use Railway credentials with only the permissions needed.

## Reference(s):

- [Railway](https://railway.app)
- [Railway Documentation](https://docs.railway.com)
- [Railway CLI Reference](https://docs.railway.com/reference/cli-api)
- [Railway Templates](https://railway.app/templates)
- [Railway CLI GitHub](https://github.com/railwayapp/cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Railway CLI commands that affect live services; users should review commands before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
