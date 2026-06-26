## Description: <br>
融合东方智慧和几何数学的交易分析系统，使用几何结构、多周期 MACD 风洞结构共振、缩量短线、基本面、市场情绪和 AI 预测信号生成股票分析评分与操作建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saitoshen](https://clawhub.ai/user/saitoshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Chinese A-share stock analysis that combines technical geometry, multi-period MACD, volume and volatility contraction, optional LLM-assisted factors, and scoring-based trading suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present placeholder or thinly supported stock analysis as actionable trading guidance. <br>
Mitigation: Treat scores and buy/sell suggestions as research prompts only and review the underlying market, financial, and risk context before acting. <br>
Risk: The full workflow asks users to store API keys in a local configuration file. <br>
Mitigation: Avoid committing config.py after adding keys, restrict file access, and prefer environment-specific secret handling where possible. <br>
Risk: The full analysis path may call external model providers. <br>
Mitigation: Use the core no-LLM script when external model calls are not desired. <br>


## Reference(s): <br>
- [太几何交易参考文档](references/technical_guide.md) <br>
- [股票基本面分析参考](references/fundamental_analysis.md) <br>
- [Tushare](https://tushare.pro) <br>
- [MiniMax](https://www.minimax.chat) <br>
- [Tencent K-line data endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style stock analysis reports with scores, signals, risk notes, and trading suggestions; scripts also print command-line text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The full workflow may call external market-data and LLM APIs; the core script avoids LLM calls.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
