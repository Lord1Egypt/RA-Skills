## Description:

Connects OpenClaw agents to the S2G visual workflow automation platform over WebSocket so agents can discover and execute workflow nodes as tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helmutsreinis](https://clawhub.ai/user/helmutsreinis)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation engineers use this skill to connect OpenClaw to S2G workflows, execute discovered workflow nodes, manage workflow operations, and inspect node schemas through S2G APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge can expose broad workflow execution capabilities to any caller that can reach its HTTP API.

Mitigation: Run the bridge on localhost or behind a firewall, add authentication before exposing execution endpoints, and connect only the S2G nodes the agent actually needs.

Risk: Bridge logs may contain execution parameters, responses, data pushes, or other sensitive workflow data.

Mitigation: Protect the log directory, reduce or disable sensitive logging where possible, and rotate or delete logs according to local data-retention requirements.

Risk: Connected S2G nodes can include high-impact operations such as database queries, workflow changes, or knowledge-base delete/update actions.

Mitigation: Review workflows and node permissions before agent use, avoid wiring destructive nodes unless required, and manually approve sensitive update or delete operations.

## Reference(s):

- [S2G Skill README](artifact/README.md)
- [S2G REST API Reference](artifact/references/api.md)
- [Deployment & Operations](artifact/references/operations.md)
- [WebSocket Protocol Reference](artifact/references/protocol.md)
- [S2G Platform](https://s2g.run)
- [ClawHub Skill Page](https://clawhub.ai/helmutsreinis/skills/s2g-workflow-engine)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Code]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript bridge code, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing outputs include setup steps and local bridge/API calls; S2G node execution responses are JSON and depend on the selected workflow node.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
