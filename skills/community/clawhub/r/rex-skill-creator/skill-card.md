## Description:

Creates and improves agent skills, including drafting skill content, setting up evaluations, benchmarking performance, optimizing trigger descriptions, and packaging releasable skill files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limoxt](https://clawhub.ai/user/limoxt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create or refine agent skills, run human-reviewed evaluation loops, benchmark behavior, optimize trigger descriptions, and package finished skill releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad creation, editing, testing, and packaging workflows for agent skills.

Mitigation: Review generated skill changes and scan the final skill before installation or release.

Risk: Packaged skill archives could unintentionally include private data, secrets, or symlinks from a skill folder.

Mitigation: Inspect archive contents before sharing, keep sensitive files out of skill directories, and avoid symlinks inside packaged skills.

Risk: Evaluation and review workflows can involve local helper scripts, subagents, and local review servers.

Mitigation: Approve local commands before execution, inspect outputs before using them, and stop any local review server after the review is complete.

## Reference(s):

- [Workflow Patterns](artifact/references/workflows.md)
- [Output Patterns](artifact/references/output-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/limoxt/skills/rex-skill-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with inline JSON and shell command examples; may also produce skill source files and packaged .skill archives through bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write SKILL.md content, eval metadata, benchmark outputs, review artifacts, and packaged .skill files when directed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
