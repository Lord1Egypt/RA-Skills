## Description:

Paste an agent instruction file and get a structured expert review of clarity, gaps, conflicts, guardrails, token efficiency, and concrete rewrites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victorosondu](https://clawhub.ai/user/victorosondu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to review AI agent instruction files, compare versions, stress test weak areas, and draft or rewrite agent instructions with concrete explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste secrets, private system prompts, or proprietary agent files into the active AI conversation.

Mitigation: Remove secrets and only submit content approved for review in that environment.

Risk: Suggested rewrites can change agent behavior or introduce misleading guidance if adopted without review.

Mitigation: Review and test revised instructions before deploying them.

## Reference(s):

- [Instruction Patterns](references/instruction-patterns.md)
- [Anti-Patterns](references/anti-patterns.md)
- [AI Tutorium](https://aitutorium.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown review with scored tables, quoted findings, suggested rewrites, and stress-test prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are recommendations based on user-pasted instruction text; the skill does not execute code or persist data.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
