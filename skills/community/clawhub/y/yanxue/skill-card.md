## Description:

Generates, saves, manages, and exports Chinese educational study-trip course plans for primary, middle, and high school programs using city, grade level, destination, theme, and duration inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmeteor8](https://clawhub.ai/user/dmeteor8)

### License/Terms of Use:


## Use Case:

Teachers, study-trip mentors, and education providers use this skill to draft structured研学 course plans, adapt plans by grade level and destination, save course files, and export Markdown plans to Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The save helper can write outside the intended storage folder when given a crafted course name.

Mitigation: Sanitize course names, reject path separators and traversal sequences, and constrain writes to the intended course directory before using scripts/manage_courses.py.

Risk: The skill can create local course-plan files and exported documents.

Mitigation: Require explicit user confirmation before save or export actions and review generated paths before execution.

Risk: Example files may contain zero-width characters.

Mitigation: Clean invisible characters from examples before using them as source material for generated course plans.

## Reference(s):

- [Skill Page](https://clawhub.ai/dmeteor8/skills/yanxue)
- [Course Template](artifact/templates/template.md)
- [Destination Reference](artifact/references/destinations.md)
- [Policy Background](artifact/references/policy-background.md)
- [User Case Style Guide](artifact/references/style-guide.md)
- [Example Course](artifact/references/example-course.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown course plans with optional shell commands for saving, listing, and exporting files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown course-plan files and DOCX exports when helper scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
