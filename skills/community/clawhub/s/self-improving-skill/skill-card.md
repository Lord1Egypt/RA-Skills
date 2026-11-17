## Description:

Learning growth coach for human skills. Input a skill goal, practice logs, constraints, and recent results; output bottleneck diagnosis, deliberate-practice plan, metrics, and the next practice session. For learning and coaching, not self-modifying agent code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn human skill goals and practice logs into bottleneck analysis, deliberate-practice plans, measurable progress reviews, and next-session guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or append local Markdown practice logs.

Mitigation: Install and run it only when local practice-tracking files are acceptable for the workspace.

Risk: The optional quick-log script has a limited filename-safety issue when skill names contain path separators or parent-directory segments.

Mitigation: Use simple skill names with letters, numbers, underscores, or hyphens until filename validation is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/self-improving-skill)
- [Skill definition template](artifact/assets/SKILL_DEFINITION_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell command snippets and local practice-log templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown practice logs when the optional quick-log script is used.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
