## Description:

Drafts and checks verifiable Codex goals and GitHub Issue work items with clear scope, constraints, and completion criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mc0571](https://clawhub.ai/user/mc0571)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to draft or validate a Codex goal or a GitHub Issue with actionable acceptance criteria, verification steps, and boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A drafted goal may authorize unintended actions in external systems or irreversible changes.

Mitigation: Review the goal's scope and action permissions before use; require confirmation for irreversible or sensitive actions.

Risk: Ambiguous or mixed-language requests may produce a Chinese draft when another language was intended.

Mitigation: Specify the preferred output language when requesting the draft.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mc0571/skills/write-a-goal)
- [Codex Follow a goal guide](https://developers.openai.com/codex/use-cases/follow-goals)
- [Goal specification](references/follow-goal-spec.md)
- [GitHub Issue specification](references/github-issue-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Single-line /goal command, goal objective, or structured GitHub Issue draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Issue mode produces a draft or review by default, not a GitHub write.]

## Skill Version(s):

0.2.2 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
