## Description:

Quiet logic guard for risky multi-skill workflows. Checks order before delete, send, booking, publishing, or other high-impact actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zc502](https://clawhub.ai/user/zc502)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Sara to audit risky multi-step tool or skill plans before destructive, externally visible, scheduling, payment, permission, or sensitive-data actions. It returns warnings and a safer suggested order when prerequisite safety steps are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sara is an advisory safety guard and should not be treated as a complete safety gate for risky actions.

Mitigation: Independently verify backups, previews, checks, permissions, and user approval before deletion, publishing, payment, booking, permission, or sensitive-data workflows.

Risk: A safe Sara result may miss workflow-specific risks outside its four ordering rules.

Mitigation: Review the full plan and confirm domain-specific prerequisites before executing high-impact or irreversible actions.

## Reference(s):

- [Sara ClawHub skill page](https://clawhub.ai/zc502/skills/sara)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance and JSON audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local advisory audit output includes is_safe, risk_level, warnings, violations, normalized_tools, and suggested_order.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog describe v0.1.0 preview behavior)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
