## Description:

Socrates helps an agent run a concise self-Q&A before planning, coding, refactoring, or delegation to clarify goals, expose assumptions, pressure-test risks, choose an approach, and define next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongyi3](https://clawhub.ai/user/hongyi3)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Socrates to add a compact planning check before complex implementation, refactoring, architecture, or delegation work. It is intended to improve execution quality by making assumptions, risks, tradeoffs, and next actions explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation may add extra structure or slow very small planning, coding, refactoring, or delegation tasks.

Mitigation: Install only when a compact planning check is desired, and disable or narrow implicit invocation in environments that support it.

## Reference(s):

- [Socrates Protocol](references/protocol.md)
- [Socrates Examples](references/examples.md)
- [Socrates ClawHub Skill Page](https://clawhub.ai/hongyi3/skills/socrates)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise Socratic Pass, Action Plan, and optional Delegation Contract sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, data access, persistence, or hidden behavior reported by security evidence.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
