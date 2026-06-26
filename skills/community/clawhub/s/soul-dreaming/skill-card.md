## Description: <br>
Progressive memory management with categorized files, indexed retrieval, and survival-merge evolution to help agents preserve critical context after compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuexian1211](https://clawhub.ai/user/xuexian1211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain workspace memory files, promote durable decisions into categorized records, and recover context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to store sensitive workspace notes in plaintext memory files. <br>
Mitigation: Review every memory write and prohibit passwords, tokens, keys, session cookies, private connection strings, and precise credential locations. <br>
Risk: The skill includes maintenance behavior that can delete, merge, archive, or otherwise alter memory records. <br>
Mitigation: Require explicit confirmation before deletion, merging, archival, heartbeat, or cron-style maintenance. <br>


## Reference(s): <br>
- [Memory Lifecycle](references/memory-lifecycle.md) <br>
- [Anti-Amnesia Checklist](references/anti-amnesia-checklist.md) <br>
- [Mount Strategy](references/mount-strategy.md) <br>
- [Survival Merge Protocol](references/survival-merge.md) <br>
- [ClawHub Release Page](https://clawhub.ai/xuexian1211/soul-dreaming) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with file templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and maintains local memory files such as INDEX.md, daily journals, categorized notes, and archive records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
