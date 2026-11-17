## Description:

Refactors AGENTS.md files into a minimal root file plus topic-specific follow-up docs using progressive disclosure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review, split, or refactor oversized AGENTS.md or CLAUDE.md guidance into a minimal root file and focused topic documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apply mode can intentionally change repository guidance files that future agents may read.

Mitigation: Use review or proposal mode first when instructions may conflict, and inspect proposed changes before applying them.

Risk: Conflicting AGENTS.md or CLAUDE.md instructions can lead to incorrect refactoring decisions.

Mitigation: Pause on conflicts, present the exact disagreement, and require the user to choose which instruction to keep before rewriting.

## Reference(s):

- [Skill Genie repository](https://github.com/Fei2-Labs/skill-genie)
- [Principles and heuristics](references/principles.md)
- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/refactor-agents-md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance, proposed file structures, and repository file edits when apply mode is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May change AGENTS.md, CLAUDE.md, or related topic guidance files in apply mode.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
