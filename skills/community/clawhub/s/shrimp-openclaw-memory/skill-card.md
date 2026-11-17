## Description:

OpenClaw Memory System gives OpenClaw agents persistent, searchable cross-session memory for user preferences, project context, facts, and conversation history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyunting555](https://clawhub.ai/user/wuyunting555)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let agents capture, retrieve, and inject relevant long-term memories across sessions while managing local storage tiers and optional x402 subscription flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic cross-session memory capture can persist sensitive or unwanted conversation data.

Mitigation: Review the skill before installation, limit where it is enabled, and avoid using it in sessions that may contain sensitive information unless retention and deletion behavior are acceptable.

Risk: Embeddings may be sent to an external provider unless local embedding mode is explicitly selected.

Mitigation: Use local embeddings for sensitive workloads or confirm the external provider, API key handling, and data-use terms before enabling remote embeddings.

Risk: The dashboard and memory APIs may expose stored memory data in under-scoped local interfaces.

Mitigation: Run the dashboard only in a trusted local environment, avoid exposing it on public networks, and stop it when memory administration is not needed.

Risk: Agent-directed x402 payment flows can spend funds or trust payment assertions without enough human control.

Mitigation: Require explicit human approval before funding wallets, set spending limits, allowlist recipients, and review payment verification behavior before enabling autonomous purchases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wuyunting555/skills/shrimp-openclaw-memory)
- [README](README.md)
- [Agent Payments Guide](AGENT-PAYMENTS.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text, JSON API responses, CLI output, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local memory records, injects retrieved memory context, and can expose dashboard and payment API responses.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
