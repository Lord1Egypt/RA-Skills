## Description: <br>
Persistent causal memory for AI agents that records decisions, tool calls, parallel work, and session history as a causally linked chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[has9800](https://clawhub.ai/user/has9800) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Raven Memory to give OpenClaw and MCP-compatible agents persistent local memory across sessions, including decisions, tool calls, and causal history for later recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cross-session memory can retain sensitive conversations, tool results, and project history with weak privacy boundaries. <br>
Mitigation: Use separate Raven databases for separate projects or users, and do not store secrets or regulated data. <br>
Risk: Recalled memory may be stale, incomplete, or misleading when reused in future sessions. <br>
Mitigation: Treat recalled memory as untrusted context and review it before relying on it. <br>
Risk: Encryption at rest is not assured by the available evidence. <br>
Mitigation: Do not assume the database is encrypted unless SQLCipher support is independently verified, and protect the database file with appropriate local access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/has9800/raven-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON tool responses with text summaries and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists agent memory in a local database configured by RAVEN_DB_PATH.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release, frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
