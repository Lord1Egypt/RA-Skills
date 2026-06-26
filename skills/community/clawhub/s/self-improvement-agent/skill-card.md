## Description: <br>
Captures learnings, errors, and corrections so agents can log recurring issues, user corrections, missing capabilities, external tool failures, outdated knowledge, and better approaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasye378](https://clawhub.ai/user/lucasye378) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture actionable learnings, command failures, corrections, and feature requests in structured Markdown files. It also guides promotion of broadly useful learnings into durable workspace guidance or new reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files and promoted prompt guidance may preserve sensitive or incorrect information across future sessions. <br>
Mitigation: Keep hooks project-scoped, review changes before writing to SOUL.md, AGENTS.md, TOOLS.md, CLAUDE.md, or similar prompt files, and avoid storing raw transcripts, credentials, tokens, personal data, or full command output. <br>
Risk: Cross-session history, send, or spawn features can transfer context beyond the current task. <br>
Mitigation: Use cross-session features only after the user has explicitly approved the specific transfer. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lucasye378/self-improvement-agent) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Skill Extraction Workflow](references/skill-extraction.md) <br>
- [Other Agents: Claude Code, Codex, Copilot](references/other-agents.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entries; optional hooks emit reminder text during agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
