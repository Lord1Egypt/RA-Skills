## Description: <br>
Unified Memory V5 provides persistent AI-agent memory with hybrid BM25, vector, and RRF search, atomic transactions, workflow support, and plugin-based integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mouxangithub](https://clawhub.ai/user/mouxangithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add long-term memory, memory search, summarization, knowledge organization, and workflow-aware recall to OpenClaw or MCP-based agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports persistent automatic memory capture and reuse. <br>
Mitigation: Review retention, deletion, scope, and disable controls before enabling the skill for sensitive conversations. <br>
Risk: The security guidance calls out cloud sync, external plugins, and HTTP server exposure as high-impact paths requiring review. <br>
Mitigation: Keep cloud sync, external plugins, and non-local HTTP listeners disabled until configuration, credentials, and network exposure are reviewed. <br>
Risk: The security guidance recommends reviewing the source that actually runs, especially install and runtime files. <br>
Mitigation: Inspect the released install and runtime files before deployment and validate that only expected memory, sync, and plugin behaviors are enabled. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mouxangithub/unified-memory) <br>
- [Artifact README](README.md) <br>
- [Artifact technical reference](SKILL.md) <br>
- [Artifact install guide](INSTALL.md) <br>
- [Artifact package metadata](package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, JavaScript examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When installed, the skill may also produce persistent memory records, search results, exports, and synchronization status through MCP or OpenClaw tools.] <br>

## Skill Version(s): <br>
5.3.0 (source: target metadata and evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
