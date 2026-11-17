## Description:

Turns mistakes, corrections, dead ends, and repeated fixes into durable improvements by helping agents capture lessons, link recurring issues, promote stable rules, and extract reusable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alethean-kaw](https://clawhub.ai/user/alethean-kaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and teams use this skill to capture meaningful corrections, non-obvious failures, missing capabilities, and stronger workflows so they can become durable workspace or repository guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files can capture secrets, tokens, private customer data, or sensitive logs.

Mitigation: Review and redact entries before storing them in .learnings; do not record secrets, tokens, private customer data, or raw sensitive logs.

Risk: Promoting unreviewed learnings into agent guidance can spread incorrect or misleading rules.

Mitigation: Review captured learnings before promotion into AGENTS.md, CLAUDE.md, TOOLS.md, SOUL.md, or reusable skills.

Risk: Broad prompt or tool hooks can add reminders in more sessions than intended.

Mitigation: Enable hooks selectively, narrow hook matchers where possible, and skip all-prompt hooks when the overhead or exposure is not acceptable.

Risk: The extraction helper writes new skill scaffolds in the workspace.

Mitigation: Run the helper only in trusted workspaces and inspect generated files before use.

## Reference(s):

- [Self Optimization on ClawHub](https://clawhub.ai/alethean-kaw/skills/self-optimization)
- [Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update learning logs, agent guidance files, hook configuration, and reusable skill scaffolds when used by an agent.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
