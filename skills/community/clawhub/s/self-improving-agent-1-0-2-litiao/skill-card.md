## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can preserve reusable project knowledge and promote important findings into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record corrections, command failures, missing capabilities, and reusable lessons into structured markdown files. It also provides optional hook setup and extraction guidance for promoting valuable learnings into durable agent or project memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist and share learned conversation data without enough consent, scoping, or redaction controls.

Mitigation: Install only when persistent self-improvement memory is intentional, keep setup project-local where possible, and avoid logging secrets, personal data, full transcripts, credentials, or sensitive business context.

Risk: Broad hook matchers can cause frequent learning reminders or collection prompts outside the intended scope.

Mitigation: Prefer narrow hook matchers, use the minimal activator-only setup when appropriate, and review hook configuration before enabling it globally.

Risk: Writing learnings into agent instruction files can preserve incorrect or misleading guidance.

Mitigation: Review every proposed update to agent memory or instruction files before promotion and scan skill changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/self-improving-agent-1-0-2-litiao)
- [Hook Setup Guide](references/hooks-setup.md)
- [Clawdbot Integration Guide](references/clawdbot-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for files such as .learnings/LEARNINGS.md, .learnings/ERRORS.md, .learnings/FEATURE_REQUESTS.md, CLAUDE.md, AGENTS.md, TOOLS.md, SOUL.md, and hook settings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
