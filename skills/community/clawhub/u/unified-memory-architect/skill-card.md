## Description: <br>
Unified Memory Architect manages dream memories with layered indexing and hybrid search for fast storage, retrieval, filtering, and statistics in the OpenClaw Agent Platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mouxangithub](https://clawhub.ai/user/mouxangithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to organize, index, query, and maintain persistent dream-memory data through CLI commands and JavaScript APIs. It is intended for OpenClaw deployments that need memory statistics, tag/date/sentiment/entity filtering, and hybrid search over stored memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marked the release suspicious because it includes persistent assistant identity, memory, heartbeat, messaging, and deletion behavior beyond the advertised memory-search scope. <br>
Mitigation: Review AGENTS.md and BOOTSTRAP.md before use, deploy only where persistent assistant behavior is intended, and disable or tightly scope heartbeat and messaging integrations. <br>
Risk: Persistent memory files such as MEMORY.md and daily notes may contain private context if used in shared or group environments. <br>
Mitigation: Avoid shared-context access to MEMORY.md, restrict workspace access, and separate personal memory files from group-chat or multi-user deployments. <br>
Risk: Memory import, cleanup, rollback, and deletion instructions can affect stored memory data. <br>
Mitigation: Back up memory data before following uninstall, rollback, migration, import, cleanup, or deletion commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mouxangithub/unified-memory-architect) <br>
- [Publisher profile](https://clawhub.ai/user/mouxangithub) <br>
- [API documentation](docs/API.md) <br>
- [Architecture documentation](docs/ARCHITECTURE.md) <br>
- [User guide](docs/USER_GUIDE.md) <br>
- [Quickstart](docs/QUICKSTART.md) <br>
- [Performance documentation](docs/PERFORMANCE.md) <br>
- [Troubleshooting guide](docs/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference memory query results, statistics, indexing behavior, and maintenance steps for OpenClaw memory data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
