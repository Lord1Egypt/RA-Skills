## Description: <br>
Automatic session continuity and task handoff across context window boundaries by monitoring context usage, saving task snapshots, and restoring recent session context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianglingling007](https://clawhub.ai/user/jianglingling007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to preserve work state across long sessions, context compaction, or session resets. It helps a new session continue active work from recent conversation tails and workspace snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve and store prior conversation text in workspace files, which may expose sensitive context if used without review. <br>
Mitigation: Install only when automatic cross-session memory is intended; review or edit the skill for sensitive work, prefer summaries over verbatim chat, and periodically inspect or delete relay snapshot, archive, heartbeat, and daily log files. <br>


## Reference(s): <br>
- [Session Relay release page](https://clawhub.ai/jianglingling007/session-relay) <br>
- [Relay Snapshot Format Reference](references/snapshot-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown snapshots and concise shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes session state to workspace memory files and may update HEARTBEAT.md or daily logs when context usage is high.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
