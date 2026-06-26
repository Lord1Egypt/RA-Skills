## Description: <br>
Kannaka Holographic Resonance Medium (HRM) provides agent guidance for persistent wave-interference memory operations, including recall, forgetting, dreaming, snapshots, swarm synchronization, collective substrate queries, and LLM provider configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickflach](https://clawhub.ai/user/nickflach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage Kannaka memory state, recall stored information, configure LLM providers, coordinate swarm memory behavior, and recover or restore HRM snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that mutate or delete persistent memory state, including forget, prune, dream, restore, and swarm health apply operations. <br>
Mitigation: Require explicit user confirmation before state-changing memory operations and prefer dry-run modes when available. <br>
Risk: The skill includes configuration paths for sensitive LLM API credentials. <br>
Mitigation: Use environment variables or a local secret manager where possible, avoid exposing keys in shared logs, and confirm the intended provider before storing credentials. <br>
Risk: The skill can start long-lived network listeners, join swarm services, update binaries, or delegate work to an external orchestrator. <br>
Mitigation: Review network endpoints and external tools before execution, and confirm with the user before update, serve, loop, swarm, or orchestrate commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickflach/skill-kannaka-memory) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nickflach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include commands that modify persistent memory state, configure credentials, contact network services, or start long-running listeners.] <br>

## Skill Version(s): <br>
2.6.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
