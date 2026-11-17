## Description:

Helps coding agents work with vvvv gamma's C# Channel system, including IChannelHub access, publishable .NET types, hierarchical propagation, subscriptions, bang channels, and spread sub-channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and engineers use this skill when building or reviewing vvvv gamma C# nodes that read, write, publish, or subscribe to public channels and hierarchical channel state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loading scene JSON through the root Project channel can update the full channel hierarchy or apply invalid project state.

Mitigation: Load only trusted JSON files, validate the schema, handle errors, and consider backups or confirmation before writing to the root Project channel.

Risk: Channel subscriptions and bidirectional writes can create feedback loops or leave stale event handlers.

Mitigation: Dispose subscriptions during node cleanup and use suppression flags when writing to channels that are also subscribed.

Risk: Creating channels with null values can crash vvvv sub-channel binding.

Mitigation: Use TryGetChannel for lookup-only retry binding and avoid TryAddChannel.

## Reference(s):

- [Channel examples](examples.md)
- [ClawHub skill page](https://clawhub.ai/tebjan/skills/vvvv-channels)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown with C# code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; it does not invoke tools, APIs, shell commands, or credentials.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
