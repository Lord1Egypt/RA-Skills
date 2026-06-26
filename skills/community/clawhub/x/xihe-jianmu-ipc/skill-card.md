## Description: <br>
Jianmu IPC is a real-time cross-AI communication hub that routes messages between OpenClaw, Claude Code, Codex, and HTTP clients through a WebSocket hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[47liu](https://clawhub.ai/user/47liu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multiple AI coding sessions through IPC messaging, session discovery, topic subscriptions, and local HTTP or WebSocket routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a local HTTP/WebSocket IPC hub that can route prompts between agent sessions. <br>
Mitigation: Set IPC_AUTH_TOKEN, keep the hub bound to trusted interfaces, and avoid sending secrets over IPC. <br>
Risk: The skill can launch additional Claude sessions and includes channel patching behavior that uses dangerous Claude flags. <br>
Mitigation: Use ipc_spawn and channel patching only when the operator accepts those risks and has reviewed the affected Claude Code environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/47liu/xihe-jianmu-ipc) <br>
- [Project homepage](https://github.com/xihe-forge/xihe-jianmu-ipc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline tool calls, JSON configuration examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces IPC messages, session listings, topic subscription updates, and setup guidance for local multi-agent coordination.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
