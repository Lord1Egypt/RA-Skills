## Description: <br>
Captures learnings, errors, corrections, and feature requests in structured markdown files so agents can reuse or promote durable workflow knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lintqiu](https://clawhub.ai/user/lintqiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture command failures, user corrections, missing capabilities, outdated knowledge, and reusable workflow improvements. The records can later be reviewed, resolved, or promoted into project or agent memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may retain user-derived conversation, error, workflow, or project details. <br>
Mitigation: Review and redact entries before writing or promoting them, and avoid storing secrets, tokens, personal data, proprietary prompts, full transcripts, or sensitive tool output. <br>
Risk: Global or every-prompt hook configuration may spread learning reminders and memory updates more broadly than intended. <br>
Mitigation: Prefer project-scoped installation and opt-in hooks; enable global hooks only after reviewing their behavior. <br>
Risk: Promoting unresolved or overly specific entries into shared memory can reinforce outdated or incorrect guidance. <br>
Mitigation: Promote only concise, reviewed lessons and update source entries with status, resolution notes, and relevant links. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Learning Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append or update .learnings markdown files and promote distilled guidance to agent memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
