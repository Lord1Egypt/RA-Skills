## Description:

Brainstorming helps agents clarify ambiguous coding requests, confirm incremental design drafts, and plan TDD-oriented implementation before writing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipoon](https://clawhub.ai/user/sipoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when a requested feature, module, or project is underspecified and needs clarification before implementation. It guides the agent to ask focused questions, present small design drafts for confirmation, and move into a test-first implementation plan only after the direction is clear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add clarification steps before implementation, which may slow simple or already-clear work.

Mitigation: Use it for ambiguous build requests and skip it for simple fixes, pure reading, pure search, or already-confirmed tasks.

Risk: Workflow text may remain in Chinese unless the host agent adapts language for the user.

Mitigation: Have the agent respond in the user's requested language and translate workflow artifacts when needed.

Risk: The workflow can lead to downstream skill-compounding or other persistent skill creation actions.

Mitigation: Review and approve any persistent skill creation or related downstream action before allowing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipoon/skills/sipoon-brainstorming)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with clarification questions, design drafts, and implementation plan tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; no executable code is bundled.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
