## Description:

AI trading memory for MT5 and forex traders that records trades, discovers patterns, and provides AI-powered reflections with strategy adjustment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zychenpeng](https://clawhub.ai/user/zychenpeng)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and traders use this skill to record trading decisions, recall similar past trades, inspect strategy performance, and generate reflections over trading behavior. MT5 users can also use the setup guidance to sync closed trades into a local TradeMemory workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and setup scripts download mutable external packages and repository content.

Mitigation: Review scripts before execution, use an isolated virtual environment, and pin package or repository versions where practical.

Risk: MT5 sync setup can place trading credentials in a local .env file.

Mitigation: Avoid live credentials where possible, restrict local file permissions, and rotate credentials if the environment is shared or compromised.

Risk: Strategy adjustments and trading reflections may be incomplete or unsuitable for live trading decisions.

Mitigation: Treat generated trading guidance as advisory and require explicit human approval before changing live trading behavior.

Risk: Configured remote API endpoints or optional LLM reflections can transmit trading data or pattern summaries outside the local machine.

Mitigation: Use only endpoints you control and verify whether optional AI reflection settings align with your data-handling requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zychenpeng/skills/tradememory)
- [Project Homepage](https://github.com/mnemox-ai/tradememory-protocol)
- [PyPI Package](https://pypi.org/project/tradememory-protocol/)
- [MT5 Sync Setup Guide](https://github.com/mnemox-ai/tradememory-protocol/blob/master/docs/MT5_SYNC_SETUP.md)
- [Tutorial](https://github.com/mnemox-ai/tradememory-protocol/blob/master/docs/TUTORIAL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with natural-language prompts, command examples, setup steps, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce trading-memory records, performance summaries, reflection guidance, and local setup commands for TradeMemory and MT5 sync workflows.]

## Skill Version(s):

0.3.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
