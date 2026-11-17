## Description:

Captures learnings, errors, feature requests, and corrections so agents can preserve useful lessons across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwoodruff86](https://clawhub.ai/user/gwoodruff86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to log command failures, user corrections, knowledge gaps, and feature requests into markdown learning files, then promote durable lessons into project or workspace guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent learning logs and promotion into future instruction files, which can preserve incorrect, misleading, or sensitive guidance if accepted without review.

Mitigation: Install only where persistent agent memory is acceptable, require explicit approval before writing or promoting learnings, and review exact diffs to AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Cross-session sharing or broad hook configuration may expose private task context or add reminders in sensitive workspaces.

Mitigation: Prefer project-level setup, avoid empty matchers that apply to all prompts, and do not use cross-session sharing for private or sensitive work.

## Reference(s):

- [Self Improving Agent on ClawHub](https://clawhub.ai/gwoodruff86/skills/self-improving-agent-grant)
- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown learning entries with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .learnings markdown files and propose promotions to agent instruction files.]

## Skill Version(s):

3.0.16 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
