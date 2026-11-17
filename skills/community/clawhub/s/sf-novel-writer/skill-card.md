## Description:

Helps users plan, draft, revise, and package science fiction stories through staged worldbuilding, plot design, character development, writing, and editing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hfaltgg2021](https://clawhub.ai/user/hfaltgg2021)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to develop science fiction projects from idea generation through worldbuilding, plot structure, character design, chapter drafting, revision, and final manuscript output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The project setup script can write outside the intended folder if a project name contains path traversal or path separator characters.

Mitigation: Use simple project names containing only letters, numbers, hyphens, or underscores; avoid path characters such as / and ..; confirm file paths before writes.

Risk: The skill can create local manuscript and project files, and some file-writing behavior is under-scoped.

Mitigation: Run it in a constrained workspace and review generated file paths and file contents before relying on them.

Risk: The README includes account-ban avoidance wording.

Mitigation: Treat that wording as unacceptable operational guidance and follow the relevant platform terms and organizational policy.

## Reference(s):

- [Phase 1: Worldbuilding](artifact/references/phase1_worldbuilding.md)
- [Phase 2: Plot Design](artifact/references/phase2_plot_design.md)
- [Phase 3: Character Design](artifact/references/phase3_character.md)
- [Phase 4: Writing](artifact/references/phase4_writing.md)
- [Phase 5: Revision](artifact/references/phase5_revision.md)
- [Science Fiction Genre Guide](artifact/references/sf_genre_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose, outlines, manuscript files, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project files when the initialization script is used.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
