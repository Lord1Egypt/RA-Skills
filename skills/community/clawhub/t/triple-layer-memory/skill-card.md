## Description: <br>
Triple Layer Memory helps AI agents preserve long-conversation context through local file memory, Mem0 vector recall, session compression, session handoff, and quality-gate workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0range-x](https://clawhub.ai/user/0range-x) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add local long-term memory, channel-aware recall, and session continuity to OpenClaw agents working through long conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically stores and reuses conversation history as local long-term memory. <br>
Mitigation: Make memory persistence explicit and opt-in, redact secrets and personal data before writes, and provide ways to inspect, disable, expire, and delete stored memories. <br>
Risk: Weak channel-isolation controls could allow memories to be loaded outside the intended channel. <br>
Mitigation: Limit which files and channels can be loaded, and verify or fix Mem0 and file-layer channel isolation before enabling automatic recall. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0range-x/triple-layer-memory) <br>
- [Publisher profile](https://clawhub.ai/user/0range-x) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Mem0 channel isolation guide](docs/mem0-channel-isolation.md) <br>
- [Memory architecture template](templates/MEMORY_ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with Python and shell command examples plus generated local memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local memory files, metadata, session handoff summaries, and initialization artifacts in the agent workspace.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
