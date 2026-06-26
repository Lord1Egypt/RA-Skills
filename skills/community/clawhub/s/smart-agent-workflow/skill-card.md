## Description: <br>
Smart Agent Workflow provides a reusable agent work methodology for task classification, WBS decomposition, P0/P1 reporting, safety checks, context management, local memory, logs, metrics, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whhaijun](https://clawhub.ai/user/whhaijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make coding or automation agents follow a structured workflow for task scoping, decomposition, progress reporting, safety checks, and context retention. It is intended for agents that can read local Markdown files and optionally run bundled shell or Python utilities for memory, logs, metrics, reports, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages local memory, logs, task briefs, metrics, and reports that may retain conversation or project data. <br>
Mitigation: Use explicit opt-in for stored data, define retention and deletion rules, and review generated memory or log files before using the skill with sensitive work. <br>
Risk: The release includes broad workflow material for team messaging, publishing, GitLab push, TAPD/Confluence, Telegram, proxy, and external AI summarization use cases. <br>
Mitigation: Remove or constrain those materials unless they match the deployment environment and have approved credentials, channels, and data-handling rules. <br>
Risk: Bundled utilities can write, move, archive, search, and report on local workspace files. <br>
Mitigation: Run utilities only in a reviewed workspace, inspect target paths before execution, and keep backups for memory and log files. <br>
Risk: The memory manager can summarize conversation history through an external AI client when configured. <br>
Mitigation: Use only approved AI clients and models, exclude secrets and regulated data from history, and disable summarization when external processing is not allowed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/whhaijun/smart-agent-workflow) <br>
- [Publisher Profile](https://clawhub.ai/user/whhaijun) <br>
- [Skill README](artifact/README.md) <br>
- [Core Agent Workflow](artifact/AGENTS.md) <br>
- [WBS Rules](artifact/process-standards/core/WBS_RULES_v3.0.md) <br>
- [Security Check](artifact/process-standards/core/SECURITY_CHECK.md) <br>
- [Context Management](artifact/process-standards/core/CONTEXT_MANAGEMENT_v2.0.md) <br>
- [Memory Compression](artifact/docs/MEMORY_COMPRESSION.md) <br>
- [Performance Monitoring](artifact/docs/PERFORMANCE_MONITORING.md) <br>
- [Multi-Agent Collaboration](artifact/docs/MULTI_AGENT_COLLABORATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, templates, and local utility scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory, log, task, metrics, report, and configuration files when its bundled utilities are used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and changelog, released 2026-03-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
