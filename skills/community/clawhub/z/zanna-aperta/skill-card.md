## Description:

MCP Bridge completo per OpenClaw con 45 tool per agenti, workspace, progetti, cron, browser, canvas, nodes, messaging, gateway, Ollama e ClawX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raidone632-create](https://clawhub.ai/user/raidone632-create)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this MCP bridge to let MCP clients operate OpenClaw agents, workspaces, projects, cron jobs, browser and canvas sessions, nodes, messaging, gateway controls, Ollama, and ClawX from one tool surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags broad OpenClaw bridge authority, including Docker commands, scheduled jobs, camera capture, and file deletion without enough guardrails.

Mitigation: Install only in a tightly controlled local environment, trust every MCP caller, and avoid exposing the server to untrusted prompts or remote clients.

Risk: Tools such as exec_docker, cron_add, camera capture, and permanent delete operations can perform high-impact local actions.

Mitigation: Review or remove these tools before general use and limit access to operators who are authorized to perform those actions.

## Reference(s):

- [Zanna Aperta ClawHub release page](https://clawhub.ai/raidone632-create/skills/zanna-aperta)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON-RPC tool responses with text content and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill exposes 45 MCP tools that can call local OpenClaw, Docker, Git, browser, canvas, node, messaging, gateway, Ollama, and ClawX actions.]

## Skill Version(s):

3.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
