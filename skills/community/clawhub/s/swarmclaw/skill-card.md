## Description: <br>
SwarmClaw teaches agents how to use the SwarmClaw AI agent runtime, including primitive tools, persistent memory, delegation, connectors, credentials, and skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help agents understand and work inside the SwarmClaw runtime. It provides guidance for selecting SwarmClaw tools, using persistent memory, handling credentials, delegating work, and interacting with connectors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain sensitive or outdated context across sessions. <br>
Mitigation: Keep memory use scoped, review stored memories for sensitive data, and clear or correct memory when it is no longer appropriate. <br>
Risk: Credentials are injected into agent command environments and can affect external services if over-scoped. <br>
Mitigation: Use least-privilege API tokens, rotate credentials regularly, and supervise workflows that use configured secrets. <br>
Risk: Host shell execution, external connectors, and agent spawning can perform actions outside the local skill text. <br>
Mitigation: Review shell commands and connector actions before execution, use sandboxing where available, and supervise delegated or spawned tasks. <br>


## Reference(s): <br>
- [SwarmClaw Skill Release](https://clawhub.ai/waydelyle/swarmclaw) <br>
- [SwarmClaw Website](https://swarmclaw.ai) <br>
- [SwarmClaw Documentation](https://swarmclaw.ai/docs) <br>
- [SwarmClaw GitHub Repository](https://github.com/swarmclawai/swarmclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; produces operational guidance for agents using SwarmClaw.] <br>

## Skill Version(s): <br>
2.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
