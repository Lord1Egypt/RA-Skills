## Description:

Share memories and state with other users through Ensue, including user, group, permission, subscription, and access-control management for memory namespaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christinetyip](https://clawhub.ai/user/christinetyip)

### License/Terms of Use:


## Use Case:

External users and teams use this skill to share memory namespaces, manage users and groups, grant or revoke access, and subscribe to memory changes. It is intended for agents that need coordinated shared-memory workflows backed by Ensue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse local Ensue credentials, including credentials from other plugin caches or ClawHub configuration.

Mitigation: Use a dedicated, least-privileged Ensue API key for this skill and avoid relying on credentials from other plugins.

Risk: Commands can immediately create or delete users and groups, change grants, revoke access, or manage subscriptions in the remote Ensue service.

Mitigation: Manually confirm create, delete, grant, revoke, subscribe, and unsubscribe commands before running them.

Risk: Troubleshooting output may expose sensitive local credential configuration.

Mitigation: Do not paste unredacted troubleshooting output, credential paths, or API key configuration into chats, logs, or support tickets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christinetyip/skills/shared-memory)
- [Ensue homepage](https://ensue-network.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ENSUE_API_KEY or configured local Ensue credentials; commands may create, delete, grant, revoke, subscribe, unsubscribe, or list remote memory-sharing resources.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
