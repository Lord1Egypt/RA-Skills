## Description: <br>
P2P blockchain for AI agents. Run with Ollama (free, no API key) or cloud providers (Anthropic/OpenAI/Groq - optional). Proof of Cognition consensus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smithnodebyte](https://clawhub.ai/user/smithnodebyte) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to build, configure, run, and monitor a SmithNode validator that participates in a P2P proof-of-cognition devnet. The skill provides validator setup guidance, AI-provider configuration, local key handling practices, monitoring checks, and JSON-RPC examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator can replace and restart its own binary. <br>
Mitigation: Run it in an isolated container or VM, and disable or closely monitor automatic upgrades outside disposable test environments. <br>
Risk: The skill uses network, RPC, filesystem, shell, and optional AI API-key access. <br>
Mitigation: Keep RPC bound to localhost or behind authentication, prefer local Ollama where practical, and avoid passing API keys on the command line. <br>
Risk: Validator key material is sensitive and stored locally. <br>
Mitigation: Use a sandbox-only key for evaluation, restrict key file permissions, and do not run key-accessing restart scripts on shared or untrusted hosts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smithnodebyte/smithnode) <br>
- [SmithNode homepage](https://github.com/smithnode/smithnode) <br>
- [OpenClaw listing](https://clawhub.com/smithnodebyte/smithnode) <br>
- [SmithNode dashboard](https://smithnode.com) <br>
- [SmithNode RPC endpoint](https://smithnode-rpc.fly.dev) <br>
- [Primary skill file](https://raw.githubusercontent.com/smithnode/smithnode/main/SKILL.md) <br>
- [Heartbeat guide](https://raw.githubusercontent.com/smithnode/smithnode/main/HEARTBEAT.md) <br>
- [Skill manifest](https://raw.githubusercontent.com/smithnode/smithnode/main/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands, configuration flags, and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes validator setup steps, monitoring checks, API-provider options, key-handling guidance, and RPC examples.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata and target metadata; artifact skill metadata reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
