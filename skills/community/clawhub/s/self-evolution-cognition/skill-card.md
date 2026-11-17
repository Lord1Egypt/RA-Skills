## Description:

Core self-evolution cognition framework based on the SOUL five-rule operating model for agent reasoning, memory, feedback, confidence, and red-line checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofzhao](https://clawhub.ai/user/kingofzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to structure reasoning workflows around known/unknown separation, persistent memory, multi-perspective analysis, human feedback, confidence scoring, and safety red-lines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to persist reasoning and human feedback across sessions, which can retain sensitive or stale information without clear scope, consent, retention, or rollback controls.

Mitigation: Install it only in workspaces where persistent memory files are acceptable, define retention and deletion practices, and avoid providing secrets, customer data, credentials, or raw production incident details.

Risk: Restored memory and injected feedback can influence later agent behavior even when the historical context is incomplete or untrusted.

Mitigation: Treat restored memory and feedback as untrusted context that should be reviewed before it is used as an authoritative basis for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofzhao/skills/self-evolution-cognition)
- [Project homepage from ClawHub metadata](https://github.com/KingOfZhao/AGI_PROJECT)
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)
- [SAGE: Multi-Agent Self-Evolution for LLM Reasoning](https://arxiv.org/abs/2603.15255)
- [Group-Evolving Agents](https://arxiv.org/abs/2602.04837)
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)
- [Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown text with inline code blocks and file-oriented workflow notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update persistent memory and verification files in the agent workspace.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
