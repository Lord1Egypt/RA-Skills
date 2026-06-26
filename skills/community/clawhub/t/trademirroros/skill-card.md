## Description: <br>
TradeMirrorOS is a workspace-level routing skill for an instruction-only trading journal framework, covering capability mapping, memory architecture, and routing into planning, journaling, review, and behavior-report sub-skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topps-2025](https://clawhub.ai/user/topps-2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-journal users use this skill to route finance journal tasks, structure trading notes and plans, generate review artifacts, and frame long-term memory recall without automating trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading notes, broker exports, ledgers, and database files can contain sensitive financial information. <br>
Mitigation: Keep broker exports, private ledgers, database files, and runtime or sync tooling under direct user control and outside public package distribution. <br>
Risk: Review outputs or historical pattern summaries could be mistaken for financial advice or trade execution instructions. <br>
Mitigation: Treat outputs as review aids, label uncertainty and sample limits, and require user review before any trading decision. <br>
Risk: Memory recall and bandit-style prioritization can overemphasize sparse or incomplete personal trading history. <br>
Mitigation: Frame historical matches as precedent or reminders rather than predictions, and keep facts separate from interpretation. <br>


## Reference(s): <br>
- [TradeMirrorOS ClawHub Page](https://clawhub.ai/topps-2025/trademirroros) <br>
- [README.md](artifact/README.md) <br>
- [TRADE_MEMORY_ARCHITECTURE.md](artifact/TRADE_MEMORY_ARCHITECTURE.md) <br>
- [finance-journal-orchestrator/references/data-contracts.md](artifact/finance-journal-orchestrator/references/data-contracts.md) <br>
- [finance-journal-orchestrator/references/operating-rhythm.md](artifact/finance-journal-orchestrator/references/operating-rhythm.md) <br>
- [trade-evolution-engine/references/evolution-algorithms.md](artifact/trade-evolution-engine/references/evolution-algorithms.md) <br>
- [EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning](https://arxiv.org/abs/2601.02163) <br>
- [HyperMem: Hypergraph Memory for Long-Term Conversations](https://arxiv.org/abs/2604.08256) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Structured text] <br>
**Output Format:** [Markdown and structured journaling or review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only outputs; no code execution, credential handling, broker execution, or remote transport.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
