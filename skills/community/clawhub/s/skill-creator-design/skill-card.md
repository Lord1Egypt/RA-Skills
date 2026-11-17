## Description:

Design generates a tailored design-project skill with supporting references to guide an agent through intake, research, solution design, review, delivery, and persistent project notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balancegsr](https://clawhub.ai/user/balancegsr)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users use this skill to create a project-specific design workflow skill for product, interaction, experience, information architecture, or visual design work. The generated skill guides the project from requirements through research, solution design, review, delivery, and follow-up summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated project skill creates and maintains local Markdown files for design progress, decisions, reviews, outputs, summaries, and feedback.

Mitigation: Install it only in workspaces where this file creation is expected, and review the generated preview before approving installation.

Risk: Generated design-project skills may activate on broad design-continuation phrases.

Mitigation: Inspect the generated skill name, trigger wording, and project directory before installation so activation scope matches the intended design project.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/balancegsr/skills/skill-creator-design)
- [Skill source README](README.md)
- [Lite skill template](references/templates/skill/lite.md)
- [Full skill template](references/templates/skill/full.md)
- [Review checklist guide](references/templates/guides/review_checklist.md)
- [Lite summary guide](references/templates/guides/summary_guide_lite.md)
- [Full summary guide](references/templates/guides/summary_guide_full.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown files and Markdown previews, with optional shell commands for packaging or installation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a generated SKILL.md, review_checklist.md, summary_guide.md, design project files, and optional ZIP packaging.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
