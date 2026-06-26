## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinqing](https://clawhub.ai/user/xinqing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to record corrections, command failures, feature requests, and recurring lessons in local markdown logs so future agent sessions can improve their behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local learning logs may capture sensitive project details if entries are copied verbatim. <br>
Mitigation: Record short, sanitized summaries and redact secrets, tokens, private keys, environment variables, and full transcripts unless the user explicitly requests that detail. <br>
Risk: Optional hooks can inspect prompts or command output and may run more broadly than intended if configured globally. <br>
Mitigation: Prefer project-level, activator-only hook setup and avoid global hooks or PostToolUse error detection when command output may contain secrets. <br>
Risk: Promoting learnings into persistent agent instruction files can preserve incorrect or sensitive guidance. <br>
Mitigation: Review each learning before promoting it into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xinqing/wx-1212) <br>
- [OpenClaw integration reference](references/openclaw-integration.md) <br>
- [Hook setup reference](references/hooks-setup.md) <br>
- [Examples reference](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends local learning, error, and feature-request records when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
