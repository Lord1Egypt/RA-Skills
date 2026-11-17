## Description:

Helps OpenClaw or Codex agents operate URUC by bootstrapping the local daemon, inspecting authoritative session and event state, discovering live commands, and routing URUC pushes first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waibiwaibig](https://clawhub.ai/user/waibiwaibig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent must participate in a URUC session, inspect authoritative runtime state, execute discovered URUC commands, and keep OpenClaw workspace guidance synchronized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote URUC messages can strongly influence the main agent session.

Mitigation: Install only for trusted URUC servers, treat URUC pushes as untrusted operational input, and review agent actions before execution.

Risk: Bootstrap and gateway flows can expose sensitive credentials in normal use.

Mitigation: Avoid plaintext or untrusted WebSocket endpoints and rotate any token exposed through bootstrap JSON output.

Risk: The skill directs agents to update workspace guidance and memory files.

Mitigation: Review proposed changes to AGENTS.md, TOOLS.md, MEMORY.md, or memory.md before allowing them to persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waibiwaibig/skills/uruc)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22 or later, URUC connection environment variables, and a reachable local OpenClaw Gateway.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
