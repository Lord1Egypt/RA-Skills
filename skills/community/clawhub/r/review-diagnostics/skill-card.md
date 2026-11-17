## Description:

Review Diagnostics is a Chinese-language manuscript review toolkit for fact-checking, reader-response simulation, structural analysis, communicative impact review, and AI-style detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and writing teams use this skill to run structured diagnostics on Chinese manuscripts, podcast scripts, and video scripts. It helps identify factual risks, weak structure, reader confusion, style drift, communicative impact issues, and AI-like writing patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checklist initializer can write outside the intended review directory when given an unsafe article name.

Mitigation: Use only simple article slugs containing letters, numbers, underscores, or hyphens; avoid slashes, dots, and absolute paths until path containment is enforced.

Risk: The workflow reads and writes local review files as part of manuscript review.

Mitigation: Run the scripts only in the intended project workspace and review file paths before executing local commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mayf3/skills/review-diagnostics)
- [Fact-check Reference](artifact/references/fact-check.md)
- [Reader Simulation Reference](artifact/references/reader-sim.md)
- [Structural Review Reference](artifact/references/structural-review.md)
- [Review Techniques Reference](artifact/references/techniques.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands]

**Output Format:** [Markdown review findings with optional JSON checklist files and terminal validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review findings are organized by required fixes, style deviations, and optional polish; local scripts can initialize and validate review completeness.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
