## Description:

Requirement Agent is a Chinese-language workflow helper that clarifies routine code-change requests and applies configurable confirmation rules before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trackoverflow](https://clawhub.ai/user/trackoverflow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to turn vague routine code-change requests into clearer requirements, then decide whether to proceed automatically or ask for confirmation before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configurable auto-execution rules may allow changes such as single-file edits, text-only edits, renames, or direct-modify requests without confirmation.

Mitigation: Review config/rules.yaml before use and tighten auto_execute or require_confirmation settings when every code change should require approval.

Risk: The workflow is intended for routine code tasks and may be insufficient for complex system design or architecture work.

Mitigation: Route new systems, architecture planning, and multi-module design work to a deeper design workflow before implementation.

## Reference(s):

- [Questioning Guide](references/questioning-guide.md)
- [Configuration Guide](references/config-guide.md)
- [Requirement Agent ClawHub Page](https://clawhub.ai/trackoverflow/skills/requirement-agent)
- [Requirement Agent Skill Page](https://skills.sh/requirement-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown conversational responses with optional code edits and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language clarification prompts and confirmation decisions governed by config/rules.yaml.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
