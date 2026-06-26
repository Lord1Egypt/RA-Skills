## Description: <br>
12维股票智能分析评分模型。基于行业、头部玩家、市场环境、管理团队、市值规模、主营业务、收入、利润、分红、回购、机构持股、大股东增减持12个维度对股票进行综合评分。触发词：股票分析、选股评分、股票评分、智能选股。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankxpj](https://clawhub.ai/user/frankxpj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to score a stock across 12 weighted business, market, and financial dimensions and generate a structured analysis report. The output is intended as informational decision support, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The stock ratings may be mistaken for financial advice. <br>
Mitigation: Treat generated ratings as informational support and have a qualified reviewer validate data, assumptions, and investment decisions. <br>
Risk: The --output option can overwrite the file path selected by the user. <br>
Mitigation: Choose an explicit report path and check for existing files before writing output. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report or JSON data produced by a local Python scoring script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run interactively, read scores from a JSON file, and write a report to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
