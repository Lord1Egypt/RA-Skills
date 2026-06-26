## Description: <br>
Captures learnings, errors, corrections, and feature requests in local Markdown files so agents can reuse and promote durable project knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashi6174](https://clawhub.ai/user/dashi6174) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record command failures, user corrections, feature requests, and reusable lessons in structured local Markdown logs. It also provides optional hook guidance for reminding agents to capture and promote high-value learnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning notes can capture sensitive project details, command output, or private context. <br>
Mitigation: Prefer project-local .learnings files, redact secrets and raw transcripts, and log short summaries unless the user explicitly requests more detail. <br>
Risk: Optional hooks run in the agent environment and the error detector can inspect command output. <br>
Mitigation: Enable hooks deliberately, inspect scripts before enabling them, prefer the activator-only setup in sensitive workspaces, and avoid global empty-match hooks. <br>
Risk: Promoting a learning into shared agent memory can spread incorrect or stale guidance. <br>
Mitigation: Review and scan summaries before promoting them into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or a new skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dashi6174/self-improving-agent2) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, hook code, and structured log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local .learnings Markdown files when the agent follows the workflow; optional hooks emit reminder text.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
