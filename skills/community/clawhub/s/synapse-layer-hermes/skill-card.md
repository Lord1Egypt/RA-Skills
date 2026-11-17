## Description:

Zero-Knowledge persistent memory layer for Hermes Agent. Provides encrypted cross-session memory, Trust Quotient (TQ) scoring, and automatic recall across ALL channels (Telegram, WhatsApp, CLI, Discord).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Hermes Agent operators use this skill to configure Synapse Layer as a persistent memory service for recalling and saving user preferences, project facts, decisions, and cross-channel context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends and retrieves memory through a remote Synapse Layer service.

Mitigation: Keep remote tool activity visible during review and confirm retention, deletion, and access-control expectations before deployment.

Risk: The security summary says the skill encourages storing credentials, tokens, private endpoints, and infrastructure details in memory.

Mitigation: Do not store secrets or private infrastructure details unless memory categories are narrowed and secret redaction guarantees are verified.

Risk: The security summary says the skill reduces user visibility of tool activity.

Mitigation: Avoid disabling tool progress in multi-user or sensitive channels unless users have another clear way to understand when remote memory tools are used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rafacpti23/skills/synapse-layer-hermes)
- [Synapse Layer Homepage](https://synapselayer.org)
- [Synapse Layer Forge](https://forge.synapselayer.org/forge)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with YAML, shell command, and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SYNAPSE_TOKEN environment variable and access to the Synapse Layer MCP service.]

## Skill Version(s):

1.1.9-b (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
