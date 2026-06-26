## Description: <br>
Persistent memory and identity continuity for AI agents, combining Second Brain files with SOULS session lineage so agents can preserve context across restarts, compaction, and context wipes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrjessek](https://clawhub.ai/user/mrjessek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give local AI agents persistent workspace memory, session lineage, and multi-agent isolation across restarts and context compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may accumulate secrets, regulated personal data, or confidential workspace details if agents store them indiscriminately. <br>
Mitigation: Avoid storing sensitive data and periodically review and prune SOUL.md, PROOF_OF_LIFE.md, MEMORY.md, daily logs, and soul files. <br>
Risk: Shared workspaces can expose one agent's memory or lineage to another agent if paths are not scoped. <br>
Mitigation: Use AGENT_NAME and scoped proof-of-life or memory paths for each agent in multi-agent workspaces. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Security](SECURITY.md) <br>
- [AGENTS protocol template](references/AGENTS-template.md) <br>
- [SOUL origin reference](references/SOUL-ORIGIN.md) <br>
- [Proof-of-life template](references/proof-of-life-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace memory files and instructions for agent startup and session handoff workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and CHANGELOG.md, released 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
