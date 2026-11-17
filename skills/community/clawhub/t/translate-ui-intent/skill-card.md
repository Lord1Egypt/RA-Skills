## Description:

Translate UI Intent helps agents turn subjective UI requests into repository-consistent frontend plans, implementation choices, and visually verified interface changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and frontend-focused agents use this skill to clarify vague UI goals, reuse existing product patterns, produce implementation-ready UI Intent Contracts, and review interface changes with rendered evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated UI decisions or code changes may be wrong when repository evidence is incomplete or ambiguous.

Mitigation: Keep uncertain decisions labeled as PROPOSED or OPEN, cite repository evidence for reuse claims, and review generated diffs before accepting changes.

Risk: Implementation or verification work may involve normal project build, test, or dev commands with repository-specific side effects.

Mitigation: Run only expected project commands in trusted workspaces, inspect command intent before execution, and review results before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wujiaming88/skills/translate-ui-intent)
- [Clarification Strategy](references/clarification-strategy.md)
- [Repository Design Discovery](references/repository-design-discovery.md)
- [UI Intent Contract](references/ui-intent-contract.md)
- [Visual Language Translation](references/visual-language.md)
- [Visual Verification](references/visual-verification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with tables, code edits, and shell command recommendations when implementation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UI Intent Contracts, reuse decisions, visual verification notes, and explicit open questions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
