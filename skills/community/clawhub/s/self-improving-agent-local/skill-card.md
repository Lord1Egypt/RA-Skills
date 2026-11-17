## Description:

Captures learnings, errors, and corrections to enable continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[healersss](https://clawhub.ai/user/healersss)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to record command failures, user corrections, missing capabilities, knowledge gaps, and recurring best practices so later sessions can reuse or promote the learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files and promoted memory can shape future agent behavior.

Mitigation: Require human review before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Learning logs and cross-session sharing can expose sensitive project, personal, or customer information.

Mitigation: Keep logs local unless sharing is intentional, and redact secrets, personal data, and customer data before storing or sending entries.

Risk: Broad hook configuration can add reminders or inspect tool output in more sessions than intended.

Mitigation: Use opt-in hooks with narrow matchers, avoid global hooks unless necessary, and review hook configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/healersss/skills/self-improving-agent-local)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and reusable entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning logs and optional hook reminders; no API keys were detected in the server evidence.]

## Skill Version(s):

1.0.10 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
