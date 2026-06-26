## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[991200448](https://clawhub.ai/user/991200448) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, feature requests, and recurring workflow improvements in Markdown memory files. The skill also guides promotion of durable lessons into agent context files and optional reminder hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files can retain sensitive prompts, transcripts, credentials, personal data, proprietary code, or tool output if users log raw details. <br>
Mitigation: Keep learning files project-scoped, log sanitized summaries instead of raw session data, and periodically audit or delete stored notes. <br>
Risk: Optional hooks can repeatedly remind agents to create or promote memory entries, which can propagate inaccurate or overly broad guidance. <br>
Mitigation: Review scripts and configured paths before enabling hooks, and require human review before promoting learnings into shared agent context files. <br>


## Reference(s): <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and learning-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-scoped notes and reminders; optional hooks inject short prompt reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
