## Description: <br>
Captures corrections, command failures, feature requests, and reusable learnings in markdown so agents can improve future work and promote durable guidance to project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorexxar](https://clawhub.ai/user/lorexxar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to log errors, corrections, knowledge gaps, feature requests, and recurring patterns during coding-agent sessions. They can then review those entries and promote broadly useful lessons into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may capture prompts, transcripts, command output, secrets, tokens, customer data, or private project details. <br>
Mitigation: Require sanitized summaries and exclude raw prompts, transcripts, command output, secrets, tokens, customer data, and private project details before writing or promoting learnings. <br>
Risk: Cross-session learning can preserve incorrect or misleading guidance. <br>
Mitigation: Review entries before promotion to CLAUDE.md, AGENTS.md, workspace files, or extracted skills, and keep promoted guidance concise and source-aware. <br>
Risk: Global or empty-match hooks can inject reminders into more sessions than intended. <br>
Mitigation: Enable hooks only where needed, keep hooks project-scoped, and review the hook scripts before enabling them. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/lorexxar/self-improving-agent-shared) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, templates, and optional hook or script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local learning logs and optional hook reminders; no fixed token limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
