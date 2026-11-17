## Description:

Viking Girlfriend is a self-hosted Norse Pagan AI companion with emotional state simulation, episodic memory, model routing, oracular responses, and ethical guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hrabanazviking](https://clawhub.ai/user/hrabanazviking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and self-hosting users can run this skill as a local AI companion that maintains conversational continuity, adapts persona state, and routes requests through local or proxied model endpoints. It is intended for interactive conversation and companion-style guidance, not regulated clinical, legal, or financial decision making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona instructions may be treated as having broad authority in a general-purpose agent.

Mitigation: Review the persona files before installation and subordinate them to the host agent's system policy, tool-use rules, and safety instructions.

Risk: Conversation context, prompts, responses, memories, and state changes can be retained in local memory and log files.

Mitigation: Run in an isolated local environment, configure log and memory retention before use, and avoid entering secrets or sensitive personal data unless retention is constrained.

Risk: The skill routes model calls through local LiteLLM and Ollama endpoints and may use authenticated external model providers configured by the operator.

Mitigation: Keep endpoints on trusted loopback or authenticated HTTPS services, protect API keys in environment variables, and verify outbound model routing before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hrabanazviking/skills/viking-girlfriend)
- [Artifact skill registration](artifact/SKILL.md)
- [Artifact security configuration](artifact/data/security_config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON-lines responses containing companion text, with terminal mode text output for local testing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime reads newline-delimited JSON on stdin and writes newline-delimited JSON on stdout in OpenClaw mode; terminal mode provides an interactive REPL.]

## Skill Version(s):

0.5.3 (source: server release metadata, released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
