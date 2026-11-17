## Description:

Provides structured questions for clarifying requirements, boundaries, business rules, and technical details before designing software tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

Testers and QA engineers use this skill to ask product managers and developers targeted questions when requirements are incomplete, test cases need review, or a bug report needs clarification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real customer, payment, identity, or production details could be exposed in prompts.

Mitigation: Use masked or synthetic examples instead of sensitive production data.

Risk: The optional broader install command uses an unpinned source.

Mitigation: Verify the source before running it, and prefer a pinned version or trusted package reference.

## Reference(s):

- [Question scenario templates](references/question-scenarios.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-question-framework)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured question list with exploration areas and clarification needs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scopes coverage to the supplied requirements and identifies uncovered areas; does not assign unique IDs.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
