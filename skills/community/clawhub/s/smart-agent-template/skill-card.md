## Description: <br>
Smart Agent Template provides workflow guidance for task triage, WBS decomposition, context management, memory handling, and automatic update checks for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whhaijun](https://clawhub.ai/user/whhaijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to standardize how agents classify work, split complex tasks, manage long context, report progress, and maintain lightweight memory across projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic updates can change local workflow files after installation. <br>
Mitigation: Disable automatic updates by default or only enable them after reviewing the configured remote and branch. <br>
Risk: Bot memory features can store conversation content and may send it to a configured AI endpoint. <br>
Mitigation: Define retention, data classification, and allowed AI endpoint rules before enabling memory-backed bot integrations. <br>
Risk: The Feishu long-connection startup path disables TLS verification and patches SDK behavior. <br>
Mitigation: Do not run the long-connection scripts until TLS verification is restored and SDK patching is removed or formally approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whhaijun/smart-agent-template) <br>
- [README](README.md) <br>
- [Core agent workflow rules](AGENTS.md) <br>
- [Multi-agent collaboration guide](docs/MULTI_AGENT_COLLABORATION.md) <br>
- [Memory compression guide](docs/MEMORY_COMPRESSION.md) <br>
- [Performance monitoring guide](docs/PERFORMANCE_MONITORING.md) <br>
- [Feishu integration guide](docs/FEISHU_INTEGRATION.md) <br>
- [OpenClaw integration guide](OPENCLAW_INTEGRATION.md) <br>
- [ChromaDB integration guide](CHROMADB_INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documents, configuration snippets, shell commands, and Python or shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional automation scripts and bot integration guidance; review commands and configuration before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
