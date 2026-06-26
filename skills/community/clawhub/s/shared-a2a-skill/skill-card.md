## Description: <br>
A2A (Agent2Agent) 协议集成技能，让 OpenClaw 智能体能够与其他实例进行点对点通信，并支持作为 Server 被调用或作为 Client 调用其他智能体。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilozhao](https://clawhub.ai/user/lilozhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure peer-to-peer Agent2Agent communication between OpenClaw instances, expose an agent card and JSON-RPC endpoint, call other agents, and optionally publish discovery or observation signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A2A messages may contain sensitive operational, personal, or confidential content. <br>
Mitigation: Treat messages as sensitive, avoid forwarding secrets or confidential content, and review the skill before enabling it in an agent environment. <br>
Risk: The Feishu observer path can forward conversations to a group without enough privacy or consent detail in the artifact. <br>
Mitigation: Keep Feishu integration disabled unless explicitly required, use dedicated low-privilege Feishu credentials, and enable it only with appropriate consent and data-handling controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilozhao/shared-a2a-skill) <br>
- [Project homepage from artifact metadata](https://gitee.com/lilozhao/shared-a2a-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, JSON-RPC, Docker, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint paths, environment variables, network addresses, and integration setup steps.] <br>

## Skill Version(s): <br>
4.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
