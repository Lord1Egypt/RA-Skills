## Description: <br>
Captures robotics autonomy failures, operational incidents, and engineering learnings to enable continuous improvement across perception, localization, planning, control, simulation, safety, and hardware integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to capture autonomy incidents, operational learnings, and feature requests across localization, planning, control, sensor fusion, hardware integration, safety, simulation, and power or thermal constraints. It also guides promotion of recurring patterns into checklists, playbooks, runbooks, or agent guidance files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent robotics learning files and promoted guidance can influence future agent behavior. <br>
Mitigation: Review entries and require human approval before writing to SOUL.md, AGENTS.md, TOOLS.md, safety checklists, playbooks, runbooks, or extracted skills. <br>
Risk: Broad automatic hooks can add reminders or react to events beyond the intended robotics workflow. <br>
Mitigation: Prefer project-level hook setup, avoid global hooks, replace empty matchers with robotics-specific patterns, deduplicate repeated events, and rate-limit reminders. <br>
Risk: Learning logs or hook inputs may contain sensitive telemetry, logs, stack traces, or infrastructure details. <br>
Mitigation: Redact secrets, private keys, sensitive endpoints, and raw command output before recording or promoting incident details. <br>


## Reference(s): <br>
- [Self-Improving Robotics release page](https://clawhub.ai/jose-compu/self-improving-robotics) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent learning logs and reminder hook configuration when the user opts in.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
