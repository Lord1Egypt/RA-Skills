## Description:

Generates structured, engineering-grade prompts for technical work such as software development, architecture, infrastructure, DevOps, APIs, AI systems, testing, observability, refactoring, audits, automation, and integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoriyai](https://clawhub.ai/user/zoriyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate concise, structured prompts for technical implementation, architecture, refactoring, audit, testing, DevOps, and automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults technical prompts to ClaudeKit Engineer and Context7 wording, which may be inappropriate when those tools are unavailable or when project context should not be sent to Context7.

Mitigation: Tell the agent to omit ClaudeKit Engineer or Context7 terms when neutral, portable prompts are needed or when Context7 should not receive project context.

## Reference(s):

- [Prompt Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured prompt sections and optional code or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include QUICK, FULL, or MASTER prompt structures depending on task scope.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
