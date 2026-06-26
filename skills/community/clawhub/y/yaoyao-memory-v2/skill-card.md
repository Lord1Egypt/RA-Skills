## Description: <br>
Yaoyao Memory Homo provides a six-layer long-term memory system with local SQLite storage, FTS5 search, optional vector search, dashboards, maintenance scripts, and sync integrations for agents that need cross-session context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taobaoaz](https://clawhub.ai/user/taobaoaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize, search, manage, and maintain persistent agent memory across sessions. It is suited for local memory workflows that may optionally add vector embeddings, cloud sync, dashboards, and administrative tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive memory content may be stored locally and may leave the machine when remote sync, embedding, or LLM-enhanced features are configured. <br>
Mitigation: Review the configured storage paths and credentials before use; keep embedding, LLM, IMA, and Samba sync disabled unless that data flow is acceptable. <br>
Risk: The dashboard and admin API expose memory, configuration, backup, cleanup, and maintenance actions. <br>
Mitigation: Keep the service bound to localhost, set and verify authentication before using admin endpoints, and avoid exposing the dashboard on shared networks. <br>
Risk: Shell embedding and auto-update behavior can perform privileged local operations. <br>
Mitigation: Keep shell embedding disabled, prefer whitelist-only execution where available, and treat update commands as privileged operations that require review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taobaoaz/yaoyao-memory-v2) <br>
- [README](artifact/README.md) <br>
- [API routes](artifact/API.md) <br>
- [Advanced configuration](artifact/ADVANCED.md) <br>
- [Memory lifecycle reference](artifact/references/memory-lifecycle.md) <br>
- [Heartbeat maintenance reference](artifact/references/heartbeat-maintenance.md) <br>
- [IMA cloud sync service](https://ima.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text, with optional JSON-style API responses from local endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files, SQLite databases, configuration files, caches, backups, and dashboard/API responses under the configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata; artifact frontmatter reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
