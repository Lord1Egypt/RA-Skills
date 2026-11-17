## Description:

Creates and upgrades reusable skills by turning conversations, workflows, and task patterns into structured SKILL.md guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxi-hub](https://clawhub.ai/user/chenxi-hub)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to create a new skill, refine an existing skill, or convert a recurring conversation workflow into a reusable SKILL.md with triggers, workflow stages, examples, and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may draw on prior conversations, project files, existing drafts, or historical skills when creating persistent instructions.

Mitigation: Provide explicit topic, time, and source boundaries before use, and review the generated SKILL.md for secrets, personal data, internal names, and unrelated project details.

Risk: The skill may persist new or overwritten skill instructions without enough confirmation.

Mitigation: Review the generated SKILL.md before it is written or overwritten, and confirm the final target path.

## Reference(s):

- [Skill Maker reference](reference/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown skill instructions, templates, checklists, and path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write persistent SKILL.md files for later agent use.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
