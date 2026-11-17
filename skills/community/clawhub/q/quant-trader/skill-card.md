## Description:

Quant Trader supports cryptocurrency strategy backtesting, paper trading, live trading, and strategy optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

External developers and trading-system operators use this skill to generate guidance, code examples, shell commands, and configuration for cryptocurrency backtesting, paper trading, live trading, and strategy optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external trading project before handling exchange credentials for live trading.

Mitigation: Review the repository and dependency list, pin or verify the exact revision, and install in a virtual environment before use.

Risk: Live trading with exchange API keys can cause financial loss or credential misuse.

Mitigation: Start with paper trading or testnet, require explicit confirmation before live trading, and use minimum-permission API keys with no withdrawal capability.

## Reference(s):

- [ClawHub Quant Trader skill page](https://clawhub.ai/zhenstaff/skills/quant-trader)
- [OpenClaw Quant GitHub repository](https://github.com/ZhenRobotics/openclaw-quant)
- [OpenClaw Quant issues](https://github.com/ZhenRobotics/openclaw-quant/issues)
- [OpenClaw Quant discussions](https://github.com/ZhenRobotics/openclaw-quant/discussions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, shell commands, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading commands and configuration that require review before live use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
