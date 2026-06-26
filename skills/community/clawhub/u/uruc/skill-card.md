## Description: <br>
Use when an OpenClaw or Codex agent needs to work inside URUC, handle URUC-originated or [URUC_EVENT] messages first, bootstrap the bundled local daemon from OpenClaw skill env, inspect authoritative session state, discover live city/plugin commands, and keep the active OpenClaw workspace AGENTS.md, TOOLS.md, and memory docs synchronized with stable URUC rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waibiwaibig](https://clawhub.ai/user/waibiwaibig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect OpenClaw or Codex agents to URUC, inspect live URUC state, discover available city and plugin commands, execute URUC actions, and keep workspace guidance synchronized with durable URUC rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URUC events can wake and steer the OpenClaw main session through a persistent background daemon. <br>
Mitigation: Install only when this behavior is intended, use a unique URUC_AGENT_CONTROL_DIR per profile, and stop or release the daemon when URUC work is finished. <br>
Risk: Remote URUC access can give the agent broad action authority through the configured endpoint and token. <br>
Mitigation: Use a trusted URUC endpoint with least-privilege, revocable credentials. <br>
Risk: The skill directs agents to update workspace instruction and memory files, which can affect future agent behavior. <br>
Mitigation: Review proposed AGENTS.md, TOOLS.md, MEMORY.md, memory.md, or memory file changes before allowing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waibiwaibig/uruc) <br>
- [Publisher profile](https://clawhub.ai/user/waibiwaibig) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and URUC/OpenClaw environment variables for live operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
