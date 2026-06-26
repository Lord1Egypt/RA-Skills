## Description: <br>
Connects OpenClaw agents to S2G over WebSocket so they can discover, execute, and manage S2G workflow nodes as tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helmutsreinis](https://clawhub.ai/user/helmutsreinis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to connect an OpenClaw agent to S2G workflows, execute connected workflow nodes, receive workflow data pushes, and manage S2G automation through documented APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge exposes workflow execution controls through a network-accessible local HTTP API that is unauthenticated by default. <br>
Mitigation: Run the bridge behind a local firewall or change it to bind to 127.0.0.1, and add authentication before exposing the port beyond trusted local agent access. <br>
Risk: Connected S2G workflows may include powerful or destructive nodes, including database, custom-code, AI, and workflow-management actions. <br>
Mitigation: Connect only trusted workflows and nodes, avoid production database or destructive custom nodes unless required, and review node schemas and parameters before execution. <br>
Risk: Bridge logs may contain node names, execution parameters, errors, and pushed workflow data. <br>
Mitigation: Treat bridge logs as sensitive, restrict log file access, and avoid passing secrets or unnecessary sensitive data through workflow payloads. <br>
Risk: The S2G WebSocket endpoint can operate without an auth secret if the OpenClaw node is left unprotected. <br>
Mitigation: Set an S2G Auth Secret on the OpenClaw node and pass the matching secret to the bridge through the CLI or S2G_SECRET environment variable. <br>


## Reference(s): <br>
- [S2G Platform](https://s2g.run) <br>
- [ClawHub Skill Page](https://clawhub.ai/helmutsreinis/s2g-workflow-engine) <br>
- [S2G REST API Reference](references/api.md) <br>
- [Deployment & Operations](references/operations.md) <br>
- [WebSocket Protocol Reference](references/protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and local HTTP API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated bridge commands, S2G workflow API calls, node execution payloads, operational checks, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
