## Description:

Helps coding agents write C# node classes for vvvv gamma, including the [ProcessNode] pattern, Update() methods, out parameters, pin configuration, change detection, stateless operation nodes, and service consumption via NodeContext.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and coding agents use this skill to draft and review C# custom nodes for vvvv gamma projects, including stateful ProcessNode classes, stateless utility operations, regions, service access, and reusable starter templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples include a ready-to-copy WebSocket server that starts enabled by default without security scoping or access-control guidance.

Mitigation: Do not copy that example verbatim; default the server off, bind to localhost unless remote access is intentional, add authentication and authorization, validate origins and messages, and document firewall and TLS requirements for non-local use.

Risk: Generated C# node guidance can introduce runtime leaks or frame-loop performance problems when resource cleanup, caching, or allocation rules are not followed.

Mitigation: Review generated nodes before use, ensure IDisposable cleanup for unmanaged or external resources, and keep Update methods allocation-conscious with explicit change detection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tebjan/skills/vvvv-custom-nodes)
- [Advanced Node Patterns](artifact/advanced.md)
- [Custom Node Examples](artifact/examples.md)
- [Custom Regions](artifact/regions.md)
- [Service Consumption and Constructor Injection](artifact/services.md)
- [Stateful node template](artifact/templates/stateful-node.cs)
- [Stateless node template](artifact/templates/stateless-node.cs)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with C# code examples and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include C# node skeletons, review guidance, and implementation notes for vvvv gamma.]

## Skill Version(s):

1.0.0 (source: server release metadata; frontmatter metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
