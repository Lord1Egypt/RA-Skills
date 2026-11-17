## Description:

Self-iteration and feedback learning engine for AI agent skills that tracks usage logs, detects performance patterns, triggers skill updates, and proposes new skill creation based on repeated request patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this shared component to log skill usage, identify repeated success or failure patterns, capture user corrections, and decide when to update existing skills or propose new dedicated skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can record interaction summaries and use them to influence future skill behavior.

Mitigation: Restrict logs to sanitized summaries, define retention and deletion rules, and review logged content before it is reused for skill updates.

Risk: The skill describes workflows that can update SKILL.md files or propose new skill creation.

Mitigation: Require explicit human approval and security review before applying any skill edits or creating new skills.

Risk: Cross-skill logging and feedback loops can broaden the effect of incorrect or sensitive observations.

Mitigation: Limit cross-skill access to an allowlist and keep shared feedback data scoped to the dependent skills that need it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bustes01/skills/self-iteration-engine)
- [OpenClaw homepage metadata](https://clawhub.ai/BusTes01/self-iteration-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with inline YAML and Markdown examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces logging formats, review-cycle guidance, update decision criteria, and new-skill proposal structure.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
