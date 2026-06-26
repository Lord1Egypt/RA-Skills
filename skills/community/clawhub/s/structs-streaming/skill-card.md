## Description: <br>
Connects to the GRASS real-time event system via NATS WebSocket so agents can receive real-time Structs game updates and react to events as they happen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to build event-driven Structs tools that monitor GRASS streams for raids, fleet movement, player creation, combat updates, inventory changes, and other real-time game events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GRASS event monitoring uses plaintext WebSocket endpoints, so event data may be unencrypted or tamperable in transit. <br>
Mitigation: Treat streamed data as advisory, prefer trusted network paths, and verify consequential decisions against authoritative Structs or chain data before acting. <br>
Risk: Broad wildcard subscriptions can collect large amounts of third-party event traffic. <br>
Mitigation: Use wildcard discovery briefly, filter noisy subjects, and narrow subscriptions to the specific player, planet, struct, fleet, or inventory subjects needed for the task. <br>
Risk: Automation examples can involve signer keys, purchases, spending, or other consequential game actions. <br>
Mitigation: Use dedicated low-permission signer keys, grant narrowly scoped permissions, require explicit approval for spending or major game actions, and log automated actions for review. <br>


## Reference(s): <br>
- [Structs Streaming Skill Page](https://clawhub.ai/abstrct/structs-streaming) <br>
- [Structs Guild Endpoint](https://public.testnet.structs.network/structs/guild) <br>
- [Structs Streaming Protocol](https://structs.ai/protocols/streaming) <br>
- [Structs Streaming Event Types](https://structs.ai/api/streaming/event-types) <br>
- [Structs Streaming Event Schemas](https://structs.ai/api/streaming/event-schemas) <br>
- [Structs Subscription Patterns](https://structs.ai/api/streaming/subscription-patterns) <br>
- [Structs Async Operations](https://structs.ai/awareness/async-operations) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell, JavaScript, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
