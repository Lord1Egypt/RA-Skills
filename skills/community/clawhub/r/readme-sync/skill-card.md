## Description:

README Sync helps coding agents read relevant README context before project work and propose confirmed README updates after code work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyqfxy](https://clawhub.ai/user/zyqfxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to keep README.md aligned with project state by reading relevant sections before work, caching noteworthy changes, and applying README updates after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read README context automatically during project work.

Mitigation: Install it only when that behavior is acceptable for the project, and limit README contents to information appropriate for agent context.

Risk: README updates or auto-initialization could introduce inaccurate project documentation if accepted without review.

Mitigation: Review pending updates and generated README content before approving sync or auto-init behavior.

Risk: The helper creates a pending-update JSON file while staging README changes.

Mitigation: Review or clear pending updates before committing repository changes.

## Reference(s):

- [README Sync release page](https://clawhub.ai/zyqfxy/skills/readme-sync)
- [README template](references/readme_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads README sections and proposes README updates; README writes require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
