## Description:

Instructions and authentication code for building headless BaaS applications with Zion.app (functorz.com). Use when integrating Zion backend features like GraphQL, actionflows, AI agents, binary assets, and payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timqin-m](https://clawhub.ai/user/timqin-m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect custom frontend applications or agent workflows to Zion.app as a headless backend. It supports authentication, runtime token retrieval, project schema lookup, GraphQL queries and mutations, subscriptions, and credential persistence for Zion projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill administers a Zion backend using developer tokens and runtime admin tokens.

Mitigation: Prefer OAuth authentication, avoid admin tokens unless the requested backend change is explicit and intended, and rotate tokens if exposed.

Risk: Credentials are persisted in .zion/credentials.yaml.

Mitigation: Keep the credentials file out of source control and backups, restrict its permissions, and review it before sharing project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timqin-m/skills/zion-baas-skill)
- [Functorz / Zion.app](https://www.functorz.com)
- [Zion runtime GraphQL API](https://zion-app.functorz.com/zero/{projectExId}/api/graphql-v2)
- [Zion Meta API](https://zionbackend.functorz.com/api/graphql)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with GraphQL examples, JSON results, YAML credential configuration, and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .zion/credentials.yaml through bundled CLI scripts and emit GraphQL query results or subscription events.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
