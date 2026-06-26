## Description: <br>
Captures learnings, errors, corrections, and feature requests so AI coding agents can preserve useful lessons and improve future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelaner](https://clawhub.ai/user/kelaner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding-agent users use this skill to record command failures, user corrections, missing capabilities, and reusable lessons in project-local markdown logs. The recorded entries can later be reviewed and promoted into durable project or agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture secrets, personal data, raw transcripts, or confidential business context. <br>
Mitigation: Use project-local storage where possible and do not log secrets, tokens, personal data, raw transcripts, or confidential business context. <br>
Risk: Broad hook activation can add reminders or error detection across agent sessions. <br>
Mitigation: Keep hooks disabled unless they are intentionally needed, and review hook configuration before enabling it. <br>
Risk: Promoting session learnings into memory or instruction files can preserve incorrect or misleading guidance. <br>
Mitigation: Require explicit review and approval before promoting entries into durable instruction, memory, or workspace files. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Logging Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project-local learning logs and memory or instruction files when the user approves.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
