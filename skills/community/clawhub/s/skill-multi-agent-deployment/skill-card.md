## Description: <br>
Deploy production-grade multi-agent fleets in OpenClaw with battle-tested scripts, cloud deployment templates, and shared memory infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinas90](https://clawhub.ai/user/abhinas90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scaffold, configure, validate, and deploy OpenClaw multi-agent fleets with shared memory, routing rules, and cloud deployment templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes cloud deployment, routing, memory-server, and deletion capabilities without enough guardrails or warnings. <br>
Mitigation: Review scripts before execution, run dry-run modes first, protect cloud credentials, narrow routing rules before production use, and back up shared memory and agent directories before reset procedures. <br>
Risk: The shared-memory REST API can expose coordination data if bound beyond localhost without controls. <br>
Mitigation: Keep the API on localhost unless authentication, authorization, and network controls are added. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abhinas90/skill-multi-agent-deployment) <br>
- [Multi-Agent Architecture Patterns](references/architecture.md) <br>
- [Structured Memory Schemas for Multi-Agent Systems](references/memory-schemas.md) <br>
- [Troubleshooting Multi-Agent Deployment](references/troubleshooting.md) <br>
- [Workflow DAG Templates for Multi-Agent Deployment](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command examples, Python scripts, shell scripts, JSON, and YAML configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment scaffolding, routing configuration, shared-memory operations, validation checks, and cloud deployment manifests for OpenClaw agent fleets.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact version history, released 2026-05-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
