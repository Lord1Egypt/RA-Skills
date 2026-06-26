## Description: <br>
Zanna Aperta is an MCP bridge that exposes 45 OpenClaw and ClawX tools for agents, workspaces, projects, cron jobs, browser and canvas control, nodes, messaging, gateway operations, Docker/Git, and Ollama. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raidone632-create](https://clawhub.ai/user/raidone632-create) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use Zanna Aperta to let an MCP-capable agent administer an OpenClaw workspace and related local services from one tool surface. It is intended for environments where broad workspace, browser, node, gateway, Ollama, Docker/Git, and ClawX actions are explicitly desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge gives agents broad OpenClaw administration powers, including delete, cron, Docker/Git, browser, canvas_eval, camera, messaging, gateway, and ClawX controls. <br>
Mitigation: Install only when that level of control is intentional; use a dedicated disposable OPENCLAW_WORKSPACE, pin OPENCLAW_BIN to a trusted binary, and require out-of-band confirmation before destructive or sensitive actions. <br>
Risk: Insufficient scoping, consent, or recovery safeguards can make unintended local changes difficult to reverse. <br>
Mitigation: Run the skill in a contained workspace, keep recoverable backups for managed state, and limit use to trusted agents and operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raidone632-create/zanna-aperta) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON-RPC tool responses containing text content and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw and Python 3.8+; optional Ollama and ClawX integrations depend on local services and paths.] <br>

## Skill Version(s): <br>
3.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
