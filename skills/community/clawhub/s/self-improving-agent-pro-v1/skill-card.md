## Description:

A framework that helps AI agents learn from mistakes, self-correct decisions, persist memory across sessions, and improve from experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mark-heartflow](https://clawhub.ai/user/mark-heartflow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a reusable capability layer for decision verification, persistent memory, reflection, self-correction, and guarded self-improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and conversation-to-code learning may retain sensitive conversations, private code, or other confidential context.

Mitigation: Use only in a contained workspace with non-sensitive inputs unless memory behavior has been reviewed and storage retention is explicitly configured.

Risk: Optional remote API use and plaintext key storage can expose real credentials or private content if enabled without review.

Mitigation: Disable remote embeddings and plaintext key storage by default, and avoid real API keys until configuration and data flow have been audited.

Risk: Self-modification, automation environment flags, and user-instruction overrides can change agent behavior beyond the user's immediate request.

Mitigation: Keep self-modification and automation gated, require human review for generated code or shell commands, and run changes in an isolated workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mark-heartflow/skills/self-improving-agent-pro-v1)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Installation Guide](INSTALL_FOR_AI.md)
- [Feature Comparison](references/feature-comparison-20260507.md)
- [Verification Methodology](references/verification-methodology.md)
- [Memory System Comparison](references/memory-system-comparison.md)
- [Reflexion](https://arxiv.org/abs/2308.07915)
- [Self-Verification](https://arxiv.org/abs/2312.09210)
- [CRITIC](https://arxiv.org/abs/2312.04445)
- [Constitutional AI](https://arxiv.org/abs/2212.08073)
- [Generative Agents](https://arxiv.org/abs/2304.03442)
- [Self-Reward](https://arxiv.org/abs/2403.00564)
- [Plan-and-Solve](https://arxiv.org/abs/2305.04091)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JavaScript examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions and reusable framework code patterns; generated changes should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, metadata.json, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
