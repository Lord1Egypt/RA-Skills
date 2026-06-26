## Description: <br>
Veritas Memory helps agents maintain layered persistent memory with state files, daily logs, long-term summaries, credential indexes, gap detection, and deep history retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moozechen](https://clawhub.ai/user/moozechen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to give an agent persistent memory workflows for state tracking, session recovery, log-backed verification, and periodic memory maintenance. It is most appropriate when the user intentionally wants the agent to maintain durable project context and credential-location indexes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain sensitive, stale, or overbroad project context. <br>
Mitigation: Review STATE.md, MEMORY.md, and memory logs before deployment; limit what may be stored; require approval before deletion or retention of sensitive entries. <br>
Risk: Credential indexing and broad credential searches can expose secrets or normalize insecure secret storage. <br>
Mitigation: Use named search scopes, require explicit approval before storing credentials, and prefer a secrets manager over plaintext files, systemd environment text, or transcript-derived indexes. <br>
Risk: Transcript and session-file searches can reveal private conversation history beyond the current task. <br>
Mitigation: Restrict history retrieval to a specific user-approved query, session, or time range, and avoid copying unrelated transcript content into memory files. <br>
Risk: Deployment and verification workflows may modify server configuration or restart services. <br>
Mitigation: Review proposed server changes and service restarts before execution; verify target hosts, commands, and rollback steps in a scoped environment. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/moozechen/veritas-memory) <br>
- [Memory Tender](references/memory-tender.md) <br>
- [STATE.md Format Specification](references/state-format.md) <br>
- [Bidirectional Verification Protocol](references/verification-loop.md) <br>
- [Write-Ahead Log Protocol](references/wal-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated memory/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update STATE.md, MEMORY.md, memory/*.md, credential indexes, and shell-script status output when used by an agent.] <br>

## Skill Version(s): <br>
4.2.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
