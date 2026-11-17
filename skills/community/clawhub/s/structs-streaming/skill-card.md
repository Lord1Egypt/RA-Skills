## Description:

Connects to the GRASS real-time event system over NATS WebSocket so agents can react to game events, monitor raids or attacks, watch player creation, track fleet movements, and build event-driven tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game automation engineers use this skill to subscribe to GRASS/NATS streams, discover event subjects, monitor Structs game activity, and build event-driven listener tools. It is most useful for real-time alerts, combat and raid monitoring, player creation watches, fleet tracking, and scoped automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended automation can trigger game transactions from unauthenticated WebSocket events.

Mitigation: Verify events through a trusted source, use narrowly delegated keys, require human approval for sensitive actions, and rate-limit reactions.

Risk: Game signing keys or delegated permissions can be over-scoped for automation agents.

Mitigation: Use a separate automation key with minimal object-specific permissions and revoke access when it is no longer needed.

Risk: Long-running listeners can create operational exposure through idle connections, excess subscriptions, or broad logs.

Mitigation: Subscribe only to needed subjects, close idle connections, limit subscriptions, and keep logs scoped to the workflow.

Risk: Unpinned client dependencies can change listener behavior after deployment.

Mitigation: Pin dependency versions before deployment and review updates before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstrct/skills/structs-streaming)
- [Structs streaming protocol](https://structs.ai/protocols/streaming)
- [Structs streaming event types](https://structs.ai/api/streaming/event-types)
- [Structs streaming event schemas](https://structs.ai/api/streaming/event-schemas)
- [Structs subscription patterns](https://structs.ai/api/streaming/subscription-patterns)
- [Struct attack event detail schema](https://structs.ai/api/integration-notes#struct_attack-event-detail-schema)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes listener patterns, subject mappings, event catalogs, and operational safety boundaries.]

## Skill Version(s):

1.25.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
