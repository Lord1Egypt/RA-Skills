## Description: <br>
Provides persistent memory management for agents with hybrid search, atomic transactions, deduplication, compression, lifecycle controls, plugins, and MCP/API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mouxangithub](https://clawhub.ai/user/mouxangithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Unified Memory to add persistent, searchable memory to OpenClaw and MCP workflows. It supports storing conversation facts, retrieving relevant context, organizing and deduplicating records, and managing memory quality over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories may include sensitive personal or work data and can persist beyond the original conversation. <br>
Mitigation: Use it only for data you intend to retain, review memory storage locations and retention settings, and avoid storing secrets or regulated data unless an approved control process is in place. <br>
Risk: Web, API, or dashboard interfaces may expose stored memories if enabled without appropriate access controls. <br>
Mitigation: Disable or firewall these interfaces by default, bind dashboards to localhost, and require authentication before any network exposure. <br>
Risk: Optional remote LLM, cloud sync, Git, or QMD integrations may move memory content outside the local environment. <br>
Mitigation: Keep remote providers and sync features disabled unless explicitly intended, and review credentials, endpoints, and sync settings before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mouxangithub/unified-memory-minimal) <br>
- [Unified Memory Documentation](artifact/docs/en/README.md) <br>
- [MCP Tools Reference](artifact/docs/en/api/mcp-tools.md) <br>
- [Configuration Guide](artifact/docs/en/getting-started/configuration.md) <br>
- [Architecture Overview](artifact/docs/en/architecture/overview.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON/tool results with inline command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist and retrieve user or workspace memory records through local files, SQLite/vector stores, MCP tools, CLI commands, and optional API or web interfaces.] <br>

## Skill Version(s): <br>
5.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
