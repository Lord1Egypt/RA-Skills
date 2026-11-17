## Description:

Workspace-level routing skill for the Finance Journal framework, covering the capability map, memory architecture, and routing into instruction-only journaling, planning, review, and behavior-reporting sub-skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topps-2025](https://clawhub.ai/user/topps-2025)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and trading-journal users use this skill to route natural-language journal, plan, review, and discipline-analysis requests into structured memory workflows. It helps preserve trade facts, hypotheses, lessons, and behavior patterns as review aids rather than trading signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading-review outputs could be mistaken for investment advice or executable trading signals.

Mitigation: Treat plans, reminders, historical matches, and skill-card candidates as review aids; the package explicitly keeps execution and automatic strategy deployment out of scope.

Risk: Private broker exports, ledgers, databases, or journal data could be exposed if users package or share runtime data.

Mitigation: Keep broker exports, private ledgers, databases, `_runtime*`, and vault/runtime data outside public packages and shared artifacts.

Risk: Users could assume the skill performs sync, repository transport, or credentialed operations.

Mitigation: Do not provide secrets, tokens, broker credentials, or remote transport credentials; keep file writes, git operations, sync, and publishing actions under direct user control.

## Reference(s):

- [TradeMirrorOS README](README.md)
- [Trade Memory Architecture](TRADE_MEMORY_ARCHITECTURE.md)
- [Data Contracts](finance-journal-orchestrator/references/data-contracts.md)
- [Operating Rhythm](finance-journal-orchestrator/references/operating-rhythm.md)
- [Evolution Algorithms](trade-evolution-engine/references/evolution-algorithms.md)
- [EverOS repository](https://github.com/EverMind-AI/EverOS)
- [EverMemOS paper](https://arxiv.org/abs/2601.02163)
- [HyperMem paper](https://arxiv.org/abs/2604.08256)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured text with JSON-shaped journaling, planning, review, and behavior-report payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only outputs; does not execute trades, sync repositories, request credentials, or operate broker accounts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
