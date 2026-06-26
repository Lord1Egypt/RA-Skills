## Description: <br>
量化策略助手：自然语言→策略生成→回测→优化→QMT模拟/实盘。三轮交互闭环。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[listolany](https://clawhub.ai/user/listolany) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quant-trading practitioners use this skill to turn natural-language strategy ideas into generated strategy code, backtests, parameter optimization runs, and optional QMT simulation or live-trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated strategies or orchestration commands can affect real trading accounts when QMT simulation or live-trading mode is used. <br>
Mitigation: Start with paper or simulation accounts, confirm the generated strategy code and run parameters, and use live trading only after a successful reviewed backtest. <br>
Risk: The skill can read trading or data credentials and may rely on local environment files for tokens. <br>
Mitigation: Provide tokens explicitly for each run when possible, avoid storing production credentials in shared environments, and verify logs do not expose secrets. <br>
Risk: The workflow can start background monitoring services and terminate processes on configured monitor ports. <br>
Mitigation: Run it in an isolated trading environment with controlled port configuration and review process activity before and after each run. <br>
Risk: A live probe order may be placed and canceled during QMT validation. <br>
Mitigation: Use a controlled account and confirm broker, account, symbol, and order-risk settings before enabling QMT validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/listolany/quant-strategy-assistant) <br>
- [QuantClaw configuration guide](https://gitee.com/GuojinQuant/quant-claw#第四步配置环境变量) <br>
- [qgdata data capability reference](qgdata-reference.md) <br>
- [qgdata user API](references/SDK_USER_API.md) <br>
- [qgdata minute-bar API](references/SDK_USER_API_STK_MINS.md) <br>
- [vnpy_qmt README](QMT-TradingClaw/vnpy_qmt/README.md) <br>
- [qgdata token service](https://quantgo.ai/data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, generated Python strategy code, shell commands, and JSON status interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create strategy files, invoke backtest and QMT orchestration commands, and summarize monitor or report URLs returned by those commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
