## Description:

A2A (Agent2Agent) 协议集成技能，用于让 OpenClaw 智能体与其他实例进行点对点通信，并支持作为 Server 被调用或作为 Client 调用其他智能体。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilozhao](https://clawhub.ai/user/lilozhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure agent-to-agent messaging, expose an A2A server endpoint, call peer agents as a client, and optionally manage registry discovery and Feishu observation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional registry and network discovery can expose private agent addresses or topology data if pointed at an untrusted registry.

Mitigation: Run A2A servers only on trusted networks and avoid publishing private IP or topology data to untrusted registries.

Risk: Feishu notifications can share conversation content with a third-party workspace.

Mitigation: Enable Feishu notifications only for conversations that are acceptable to share with that workspace.

Risk: The security guidance notes that required runtime files may be missing from the released artifact.

Mitigation: Confirm the required runtime files are available from the publisher before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilozhao/skills/shared-a2a-skill)
- [Project homepage](https://gitee.com/lilozhao/shared-a2a-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, JSON-RPC, Docker, environment-variable, and JavaScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes A2A server/client setup, static peer configuration, optional registry discovery, and Feishu notification configuration.]

## Skill Version(s):

4.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
