## Description: <br>
Captures learnings, errors, and corrections so agents can log failures, user corrections, feature requests, knowledge gaps, and reusable improvements for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huihuilu](https://clawhub.ai/user/huihuilu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture task learnings, command errors, user corrections, and feature requests in structured markdown logs. It also provides optional hook setup guidance for reminders and error-pattern detection in trusted workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist agent behavior, corrections, and operational details in learning files. <br>
Mitigation: Use project-scoped learning files, sanitize entries, and avoid logging secrets, tokens, raw transcripts, sensitive business data, or full source and configuration files. <br>
Risk: Optional hooks can inject reminders broadly and inspect command output for error patterns. <br>
Mitigation: Enable hooks only in trusted workspaces, prefer the minimal activator hook by default, and require review before broad or global hook configuration. <br>
Risk: Promoting learnings into agent instruction files can introduce incorrect or misleading guidance. <br>
Mitigation: Review proposed promotions before writing to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions. <br>
Risk: Package metadata is inconsistent with the skill identity and dependency expectations. <br>
Mitigation: Review the publisher, skill identity, and declared gog dependency before installation or release approval. <br>


## Reference(s): <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and structured log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings markdown files and may provide opt-in hook configuration guidance.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
