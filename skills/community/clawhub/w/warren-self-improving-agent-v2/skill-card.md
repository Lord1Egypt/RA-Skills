## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for AI coding-agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengyz3327-design](https://clawhub.ai/user/chengyz3327-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture command failures, user corrections, missing capabilities, and recurring best practices as markdown learning records that can later be reviewed or promoted into project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent memory from conversation-derived context, which can retain secrets, personal information, customer data, raw transcripts, or sensitive command output if used carelessly. <br>
Mitigation: Decide where `.learnings/` should live before enabling the workflow, redact sensitive content before logging, and review entries before promotion to long-term project or workspace memory. <br>
Risk: Optional always-on hooks can inject reminders broadly across sessions and increase the chance of over-collecting context. <br>
Mitigation: Keep hook usage opt-in, avoid global always-on activation unless it is needed, and use the minimal hook configuration for the target agent. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates learning logs, error records, feature-request records, hook reminders, and skill scaffolds.] <br>

## Skill Version(s): <br>
3.0.7 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
