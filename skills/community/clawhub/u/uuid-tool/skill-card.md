## Description: <br>
Generate universally unique identifiers (UUIDs) in versions v1, v4, v5, v7, and nil format, with bulk generation and namespace-based deterministic IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate, inspect, or format UUIDs for distributed systems, database keys, idempotency tokens, and scripted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented UUID feature set is broader than the bundled script implementation. <br>
Mitigation: Validate the installed command behavior before relying on v7, nil UUID, parsing, or JSON output workflows. <br>
Risk: UUID v1 generation can reveal time-related metadata and may expose host-derived information depending on the runtime implementation. <br>
Mitigation: Use UUID v4 for opaque public identifiers when timestamp or host metadata disclosure is unacceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/uuid-tool) <br>
- [Publisher Profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Guidance] <br>
**Output Format:** [Plain text UUID strings with command examples and optional JSON-style output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bulk generation, uppercase formatting, compact no-hyphen formatting, and namespace-based deterministic UUID options are described by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
