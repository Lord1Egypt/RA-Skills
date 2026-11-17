## Description:

Smart Agent Workflow provides agent work-method guidance for task classification, WBS decomposition, P0/P1 reporting, safety checks, context management, memory, collaboration, and performance monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whhaijun](https://clawhub.ai/user/whhaijun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give AI coding or operations agents a consistent workflow for classifying tasks, decomposing complex work, reporting progress, checking safety, preserving context, and coordinating multiple agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and log files may retain private data or instruction-like content.

Mitigation: Review or disable memory features, restrict writable locations, and treat stored memory as lower priority than system, developer, and current user instructions.

Risk: Setup guidance includes curl-to-shell, unpinned npx, and unprotected .env patterns.

Mitigation: Use pinned and verified installation sources, avoid direct pipe-to-shell execution, and protect .env files with appropriate local permissions and secret handling.

Risk: Memory storage keyed by user-controlled identifiers can write or read the wrong local files if identifiers are not constrained.

Mitigation: Sanitize and scope user identifiers, isolate storage per workspace or user, and prevent path traversal or shared-file collisions.

Risk: Bundled scripts can create, move, or overwrite local memory, log, metrics, report, and task files.

Mitigation: Run scripts only in an intended workspace, review target paths before execution, and use least-privilege filesystem access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whhaijun/skills/smart-agent-workflow)
- [Core Agent Workflow](AGENTS.md)
- [WBS Decomposition Rules](process-standards/core/WBS_RULES_v3.0.md)
- [Task Reporting Rules](process-standards/core/TASK_REPORTING_v3.0.md)
- [Security Check Rules](process-standards/core/SECURITY_CHECK.md)
- [Context Management](process-standards/core/CONTEXT_MANAGEMENT_v2.0.md)
- [Multi-Agent Collaboration](docs/MULTI_AGENT_COLLABORATION.md)
- [Memory Compression](docs/MEMORY_COMPRESSION.md)
- [Performance Monitoring](docs/PERFORMANCE_MONITORING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and reusable templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update local memory, logs, metrics, reports, and task files when those workflows are enabled.]

## Skill Version(s):

1.2.0 (source: server release; changelog v1.2.0 dated 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
