## Description:

Connects OpenClaw agents to the Zynd AI Network to discover, register, call, and receive requests from other agents with optional x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atmegabuzz](https://clawhub.ai/user/atmegabuzz)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to connect an OpenClaw agent to the Zynd AI Network for agent discovery, registration, webhook-based messaging, and paid requests. It supports workflows where an agent delegates tasks to specialized agents or exposes its own capabilities to the network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The webhook server can expose incoming agent messages and identity data on network-facing endpoints.

Mitigation: Bind the server to localhost where possible, place public deployments behind authentication and TLS, and disable or protect the /messages endpoint.

Risk: Requests may send user prompts, agent identity data, and task content to third-party agents.

Mitigation: Avoid private, regulated, or sensitive data in delegated tasks and review target agents before sending requests.

Risk: Paid calls can authorize x402 micropayments from the configured agent wallet.

Mitigation: Use a low-privilege key and wallet with minimal funds, and require explicit review before enabling --pay for a request.

Risk: Setup installs and runs the external zyndai-agent Python SDK.

Mitigation: Review the SDK version and install in an isolated environment before using the skill in a trusted workspace.

## Reference(s):

- [Zynd AI Network](https://zynd.ai)
- [Zynd Dashboard](https://dashboard.zynd.ai)
- [Zynd Docs](https://docs.zynd.ai)
- [Zynd API Reference](references/api.md)
- [Zynd AI Agent SDK](https://github.com/Zynd-AI-Network/zyndai-agent)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/atmegabuzz/skills/zynd-network)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON command-line output with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .agent-<name>/config.json files and print registry, webhook, payment, and message details to stdout.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
