## Description: <br>
Persistent federated memory for OpenClaw agents, including boot handshake, handoff, decision, and escalation surfaces backed by a Stigmem node. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[offbyonce](https://clawhub.ai/user/offbyonce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect an agent to a self-hosted Stigmem node for persistent memory, handoffs, decision logging, and escalations during evaluation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Stigmem API key and connects to an external memory node. <br>
Mitigation: Use a dedicated least-privilege API key, rotate it regularly, and revoke it immediately if compromised. <br>
Risk: Retrieved memory can contain stale, poisoned, or prompt-injection content. <br>
Mitigation: Treat retrieved memory as untrusted data, append it after the hardcoded system prompt, and avoid injecting summaries in high-stakes or irreversible workflows. <br>
Risk: Facts written through the adapter persist and may propagate through federation scopes. <br>
Mitigation: Use local scope for scratch memory, restrict federation scopes, and explicitly retract incorrect facts. <br>
Risk: The dependency range targets an alpha Stigmem connector line. <br>
Mitigation: Pin exact dependency versions in repeatable environments and review release notes before upgrades. <br>


## Reference(s): <br>
- [OpenClaw connector guide](https://docs.stigmem.dev/en/latest/docs/guides/connectors/openclaw) <br>
- [Stigmem project site](https://stigmem.dev) <br>
- [Stigmem plugin catalog](https://docs.stigmem.dev/en/latest/docs/plugins) <br>
- [OpenClaw adapter limitations](https://github.com/eidetic-labs/stigmem/blob/main/LIMITATIONS.md#9-running-the-openclaw-bundled-adapter-as-is) <br>
- [ClawHub skill page](https://clawhub.ai/offbyonce/stigmem-node) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STIGMEM_URL and STIGMEM_API_KEY; optional agent identity and handoff allowlist environment variables control runtime scope.] <br>

## Skill Version(s): <br>
1.0.9 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
