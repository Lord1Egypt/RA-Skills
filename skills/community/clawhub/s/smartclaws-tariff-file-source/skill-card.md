## Description:

Local tariff data source contract for SmartClaws master agents that defines the tariff snapshot file schema and how to use it during control decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduv09](https://clawhub.ai/user/eduv09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external SmartClaws users use this skill to configure a local tariff JSON snapshot as an off-chain data source for master-agent control decisions. The skill helps agents interpret current and lookahead electricity price tiers while handling stale, missing, or malformed tariff data conservatively.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A misconfigured snapshotFile could point the agent at the wrong local JSON file.

Mitigation: Confirm the configured snapshotFile points only to the intended tariff snapshot before installing or running a connected master agent.

Risk: Stale, missing, or malformed tariff data could lead to incorrect control decisions.

Mitigation: Treat stale or malformed tariff data conservatively, report the tariff source issue, and avoid inventing future tariff values beyond the provided lookahead.

Risk: A connected agent could misuse the tariff source by changing the file or publishing local tariff data unexpectedly.

Mitigation: Use the skill as a read-only local source and publish tariff data to device channels only when the owner explicitly instructs it.

## Reference(s):

- [SmartClaws project homepage](https://github.com/skalenetwork/smartclaws)
- [ClawHub skill page](https://clawhub.ai/eduv09/skills/smartclaws-tariff-file-source)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with YAML configuration and JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; the skill expects a workspace-configured local tariff JSON snapshot path.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
