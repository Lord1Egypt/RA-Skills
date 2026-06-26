## Description: <br>
Smart Memory Plus provides a zero-dependency local memory and context compression system for OpenClaw agents, including WAL-backed session state, typed memory extraction, BM25 search, temporal decay, and session compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgjq](https://clawhub.ai/user/zgjq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain durable local memory for OpenClaw sessions, extract useful conversation facts, search prior memories, compact long sessions, and run memory hygiene tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists conversation-derived data in local memory files and indexes. <br>
Mitigation: Install only when durable local agent memory is desired, and periodically inspect or purge stored memories and indexes. <br>
Risk: The health-check helper has filename handling risk for crafted local /tmp cache filenames on shared machines. <br>
Mitigation: Review or fix memory_health.sh before running health checks in shared environments. <br>
Risk: State restoration from untrusted files can reintroduce unwanted or unsafe session context. <br>
Mitigation: Avoid restoring state from untrusted files and prefer dry-run modes for decay and maintenance workflows. <br>


## Reference(s): <br>
- [Memory Schema Reference](references/memory_schema.md) <br>
- [Memory Extraction Guide](references/extraction_prompt.md) <br>
- [Session Compaction Guide](references/compaction_prompt.md) <br>
- [Decay & Archival Rules](references/decay_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory files, local JSON cache files, SQLite index data, and shell/Python command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [All documented workflows are local-only and use Python standard library scripts plus optional Bash helpers.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
