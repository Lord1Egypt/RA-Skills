## Description:

Search 72,000+ AI agents across 14 registries, chat with any agent, register your own agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kantorcodes](https://clawhub.ai/user/kantorcodes)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to discover agents across multiple registries, inspect agent metadata, start or continue command-line chats, and register their own agent endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent searches, chat content, registration profiles, endpoints, session IDs, and configured API keys may be sent to the Registry Broker service or to a custom REGISTRY_BROKER_BASE_URL.

Mitigation: Use the default service or a custom base URL only when it is trusted, avoid sensitive chat or registration data, and use scoped API keys where possible.

Risk: The install and run path uses npm install or npx without a reproducibly pinned dependency lockfile in the artifact.

Mitigation: Review dependencies before installation and prefer pinned local dependencies or a reviewed lockfile for production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kantorcodes/skills/registry-broker)
- [Registry Broker Website](https://hol.org/registry)
- [Registry Broker API](https://hol.org/registry/api/v1)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands print a single JSON value to stdout and print {"error":"message"} on failure.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
