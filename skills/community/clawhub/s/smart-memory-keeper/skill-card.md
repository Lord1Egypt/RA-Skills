## Description: <br>
Smart Memory Keeper helps OpenClaw agents preserve local task state, daily journals, and project index notes across new sessions using a three-tier memory workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porkapple](https://clawhub.ai/user/porkapple) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let OpenClaw restore recent work context after a new session, maintain local task state, and periodically consolidate memory notes. It is most relevant for users who want persistent, human-readable workspace memory without an external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can capture sensitive project details if users allow secrets or credentials to be written into task notes or journals. <br>
Mitigation: Avoid storing secrets in memory files, review generated memory content before saving, and periodically inspect or prune ~/.openclaw/workspace/memory and MEMORY.md. <br>
Risk: First-run initialization reads recent session history to bootstrap tasks.md when the task file is empty. <br>
Mitigation: Require user confirmation before saving extracted task state and review the proposed tasks before writing them to disk. <br>
Risk: The setup flow appends memory-loading behavior to agent configuration files, which changes what future sessions read at startup. <br>
Mitigation: Review the AGENTS.md and HEARTBEAT.md snippets before applying them, and selectively apply only the rules needed for the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/porkapple/smart-memory-keeper) <br>
- [Formats](references/formats.md) <br>
- [Dream Consolidation](references/dream-guide.md) <br>
- [Install Snippets](references/install-snippets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file templates, and local memory-file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable local memory files under the OpenClaw workspace and setup snippets for AGENTS.md and HEARTBEAT.md.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
