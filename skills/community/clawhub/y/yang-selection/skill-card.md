## Description:

杨永兴尾盘选股法 - 腾讯财经实时筛选，智能市值缓存

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxyu94](https://clawhub.ai/user/dxyu94)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to screen Chinese A-share main-board stocks near market close using Tencent Finance realtime quotes, Baostock historical data, and Yang Yongxing-style filtering criteria. It supports terminal-based candidate review and local market-cap caching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Realtime quote data is fetched over plaintext HTTP and could be manipulated on untrusted networks.

Mitigation: Run only on trusted networks and verify any candidate stock data against trusted market-data sources before acting on it.

Risk: The skill outputs stock-screening candidates that may be mistaken for verified financial advice.

Mitigation: Treat output as an analytical screen only and require independent financial review before trading decisions.

Risk: Python dependencies and package install behavior may introduce supply-chain risk.

Mitigation: Install in an isolated environment, avoid npm install for this package, and pin and review Python dependencies before running.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxyu94/skills/yang-selection)
- [ClawHub publisher profile](https://clawhub.ai/user/dxyu94)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Terminal text with tabular stock candidates and a local JSON market-cap cache.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, Python data dependencies, a main_board_stocks.json input file, and market-session access to realtime quote data.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
