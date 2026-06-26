## Description: <br>
Captures agent learnings, errors, corrections, and feature requests in Markdown logs so future sessions can improve project guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f1zzyw](https://clawhub.ai/user/f1zzyw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to record corrections, failed commands, missing capabilities, and reusable practices. They can review those logs and promote broadly applicable entries into project instruction files after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs and promoted instruction files can influence future agent behavior. <br>
Mitigation: Review entries before promotion and require user approval before changing AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instruction files. <br>
Risk: Conversation-derived logs may capture secrets or private transcript details. <br>
Mitigation: Do not record credentials or sensitive transcript content, and redact logs before keeping or sharing them. <br>
Risk: Optional external repo files or hooks may change agent behavior if enabled without review. <br>
Mitigation: Inspect external files and hook scripts before enabling them, and decide in advance which files the skill may modify. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/f1zzyw/s1kasl-askdjna) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates local .learnings/*.md logs and may propose promotion into agent instruction files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
