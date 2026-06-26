## Description: <br>
基于七大哲学理论，提供多维度评分和实时数据的智能股票诊断和操作建议系统。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
投资研究人员和个人投资者可用该技能按股票代码生成结构化诊断报告，结合实时行情、基本面、技术面、行业面、消息面、资金面和估值面进行评分。输出可辅助研究和决策准备，但不应替代专业金融建议。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send stock symbols and query timing to Tencent Finance. <br>
Mitigation: Use it only when that data sharing is acceptable and avoid including sensitive portfolio details unless necessary. <br>
Risk: The artifact includes sample code that disables TLS certificate and hostname verification. <br>
Mitigation: Keep normal HTTPS certificate and hostname verification enabled when implementing data requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horizoncove/tianshu-stock) <br>
- [Tencent Finance quote API example](https://qt.gtimg.cn/q=sh603127) <br>
- [Source skill artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown diagnostic report with real-time stock data, theory-by-theory analysis, numeric scores, ratings, and operating guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a stock code and depends on Tencent Finance API availability for live market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
