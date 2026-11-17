## Description:

提供基于 TqSdk 的量化策略开发、回测和优化，涵盖趋势、套利、多因子等 61 种策略模板。

This skill is for research and development only.

## Publisher:

[gaingush](https://clawhub.ai/user/gaingush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use this skill to inspect, adapt, debug, and compare TqSdk-based futures trading strategy templates for research, simulation, backtesting, and optimization. It supports strategy selection across trend, mean-reversion, arbitrage, multi-factor, and machine-learning-assisted patterns before any live trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled strategy files include plaintext TqSdk credential placeholders and sample credentials.

Mitigation: Do not use bundled plaintext credentials, rotate any exposed credentials that belong to you, and keep real TqSdk credentials outside source files.

Risk: Executable strategy code can change orders or target positions and may affect financial accounts if configured for live trading.

Mitigation: Run only in TqSim or another simulation account unless live trading has been intentionally configured, each strategy's order logic has been reviewed, and position and loss limits are set.

Risk: Backtests and historical strategy examples may not predict future live-market performance.

Mitigation: Treat the bundled strategies as research material, perform independent validation, and avoid presenting outputs as investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaingush/skills/tqsdk-quant-strategies)
- [TqSdk Official Documentation](https://doc.shinnytech.com/tqsdk/latest/)
- [TqSdk Quickstart](https://doc.shinnytech.com/tqsdk/latest/quickstart.html)
- [TqSdk API Reference](https://doc.shinnytech.com/tqsdk/latest/reference/index.html)
- [TqSdk GitHub Repository](https://github.com/shinnytech/tqsdk-python)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code references and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reference bundled Python strategy files and should preserve simulation-first risk guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
