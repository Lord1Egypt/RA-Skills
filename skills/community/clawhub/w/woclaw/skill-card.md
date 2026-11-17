## Description:

Connect to WoClaw Hub for shared memory and multi-agent topic messaging between AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingp14](https://clawhub.ai/user/xingp14)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use WoClaw to let AI agents coordinate through topic-based messaging and share context in a global key/value memory pool across OpenClaw instances or compatible frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext hub connections can expose agent IDs, topic messages, or shared memory content when used outside trusted local networks.

Mitigation: Prefer wss:// and https:// endpoints with valid TLS for any non-local hub.

Risk: Shared global memory and topic messages may contain secrets, private prompts, or sensitive personal data visible to trusted connected agents.

Mitigation: Do not place secrets, credentials, private prompts, or sensitive personal data in shared memory or topic messages; limit hub tokens, topics, and memory access to trusted agents only.

Risk: External installs and container images can change over time if they are not pinned.

Mitigation: Use a pinned, verified package and container digest before installing or deploying the hub.

## Reference(s):

- [WoClaw GitHub repository](https://github.com/XingP14/woclaw)
- [WoClaw ClawHub skill page](https://clawhub.ai/xingp14/skills/woclaw)
- [Publisher profile](https://clawhub.ai/user/xingp14)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with slash commands, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WebSocket/REST endpoint settings, topic commands, and shared-memory key/value operations.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
