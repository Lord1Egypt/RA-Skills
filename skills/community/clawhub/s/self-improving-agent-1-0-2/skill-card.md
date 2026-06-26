## Description: <br>
Captures learnings, errors, corrections, and feature requests so coding agents can record, review, and promote reusable project knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TXMERLXN](https://clawhub.ai/user/TXMERLXN) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain project-local learning logs for failed commands, user corrections, missing capabilities, API or tool failures, outdated assumptions, and recurring better practices. It also guides review and promotion of broadly useful learnings into project memory or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived learnings may persist secrets, personal data, raw transcripts, tokens, or full command outputs. <br>
Mitigation: Redact sensitive data before recording or sharing learnings, and keep logs project-local by default. <br>
Risk: Promoted learnings can introduce incorrect or misleading durable instructions into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions. <br>
Mitigation: Review proposed changes to future instruction files before they are used by agents. <br>
Risk: Optional hooks can run reminder or error-detection scripts repeatedly and may broaden the skill's effect beyond the intended project. <br>
Mitigation: Avoid global hooks unless the scripts and configuration have been audited; prefer explicit project-scoped setup. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/TXMERLXN/self-improving-agent-1-0-2) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Clawdbot integration guide](references/clawdbot-integration.md) <br>
- [Entry examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with fenced Markdown, JSON, and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings files and optional project memory or hook configuration when the user approves those changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
