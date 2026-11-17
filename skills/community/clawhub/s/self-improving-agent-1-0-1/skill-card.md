## Description:

Captures learnings, errors, feature requests, and corrections so agents can preserve recurring project knowledge in markdown and promote important lessons to project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pntrivedy](https://clawhub.ai/user/pntrivedy)

### License/Terms of Use:


## Use Case:

Developers and AI coding-agent users use this skill to log command failures, user corrections, feature requests, knowledge gaps, and reusable fixes in structured markdown files. It also guides review and promotion of broadly useful learnings into project memory or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable learning logs may capture sensitive prompts, credentials, customer data, proprietary snippets, or raw error output.

Mitigation: Sanitize entries before writing them, keep .learnings local or gitignored for sensitive projects, and avoid recording secrets or private content.

Risk: Automatic hook reminders can encourage broad logging without enough user control.

Mitigation: Enable hooks only when explicitly desired, prefer project-scoped configuration, and use scoped matchers rather than global activation.

Risk: Promoting unreviewed entries into CLAUDE.md, AGENTS.md, or Copilot instructions can preserve incorrect or sensitive guidance.

Mitigation: Require human review before promotion and scan proposed memory updates for correctness, sensitivity, and relevance.

## Reference(s):

- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Release Page](https://clawhub.ai/pntrivedy/skills/self-improving-agent-1-0-1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .learnings markdown records and suggest project-memory updates when the user chooses to apply the guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
