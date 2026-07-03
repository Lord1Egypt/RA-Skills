## Description: <br>
Helps coding agents capture corrections, errors, feature requests, and reusable learnings so they can improve future work across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep lightweight markdown records of mistakes, corrections, knowledge gaps, and requested features, then promote stable lessons into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may capture sensitive conversation details, secrets, command output, or environment data if used carelessly. <br>
Mitigation: Follow the security guidance to redact secrets and prefer short summaries or redacted excerpts over raw transcripts, full command output, or source/config dumps. <br>
Risk: Optional hooks can add frequent reminders and, for error detection, inspect command output for error patterns. <br>
Mitigation: Keep hooks disabled unless the workspace owner wants them, prefer the activator-only setup, and enable command-output error detection only in trusted projects. <br>
Risk: Promoting learnings into shared workspace memory can spread inaccurate or overly broad guidance across future sessions. <br>
Mitigation: Review entries before promotion, keep promoted rules concise and evidence-based, and use trusted environments for cross-session sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-self-improving-agent) <br>
- [Entry examples](artifact/references/examples.md) <br>
- [Hook setup guide](artifact/references/hooks-setup.md) <br>
- [OpenClaw integration guide](artifact/references/openclaw-integration.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command, configuration, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append local .learnings markdown files and may scaffold skill files when the extraction helper is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
