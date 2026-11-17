## Description:

Create, design, review, and self-improve agent skills following best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenkawa](https://clawhub.ai/user/sensenkawa)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent builders use this skill to design, draft, validate, package, and iteratively improve agent skills with file-grounded workflows and review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt broad local discovery and comparison of third-party skill instructions.

Mitigation: Run it in a constrained workspace, review requested reads outside the project, and treat imported skill text as evidence for comparison rather than trusted instructions.

Risk: The skill can write persistent evolution records, validation summaries, and instruction changes.

Mitigation: Require a diff review and explicit approval before changes are kept in skill instructions, reference files, or evolution logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenkawa/skills/zao-skill)
- [Design Gate](references/design-gate.md)
- [Skill Search Sources & Strategy](references/search-compare.md)
- [Skill Evolution](references/skill-evolution.md)
- [Verification Guide](references/verification-gate.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with file edits, checklists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce skill source files, validation summaries, .wip notes, and packaged .skill archives when requested.]

## Skill Version(s):

0.8.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
