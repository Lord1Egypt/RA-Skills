## Description:

Generates Chinese after-class review material and practice homework for Agent Skill lessons, including separated assignment and reference-answer Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinnxinn](https://clawhub.ai/user/yinnxinn)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, course authors, and developers use this skill to turn Agent Skill lesson content into concise review notes, tiered exercises, scoring criteria, and complete reference answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes two topic-named Markdown files in the active workspace, which could collide with similarly named existing files.

Mitigation: Review the proposed filenames before accepting output in workspaces that already contain lesson or homework Markdown files.

Risk: Generated teaching material or reference code may contain incomplete or misleading guidance if used without review.

Mitigation: Have an instructor or maintainer review the assignments, scoring criteria, and runnable examples before distributing them to students.

## Reference(s):

- [Homework Design](references/homework-design.md)
- [Agent Skill Course Knowledge](references/skill-knowledge.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance, Files]

**Output Format:** [Two Markdown files: assignment prompts and separated reference answers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes topic-named homework and answer files in the active workspace; reference answers may include complete SKILL.md and script examples.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
