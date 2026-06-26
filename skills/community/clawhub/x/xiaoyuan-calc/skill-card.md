## Description: <br>
A mathematical assistant that uses LaTeX input to run scientific calculations, solve equations and inequalities, and return detailed calculation steps through Xiaoyuan AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liutengky](https://clawhub.ai/user/liutengky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to ask an agent for LaTeX-formatted arithmetic, scientific calculations, equation solving, inequality solving, and step-by-step math explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends each user-entered math expression to Xiaoyuan/Yuanfudao's remote calculation service. <br>
Mitigation: Avoid entering confidential financial figures, proprietary formulas, private homework or work data, personal information, or other sensitive expressions. <br>
Risk: The helper script depends on the Python requests package being available in the runtime. <br>
Mitigation: Confirm the agent environment has requests installed before relying on the skill in a workflow. <br>
Risk: Calculation accuracy and availability depend on the remote service response. <br>
Mitigation: Review important answers before using them for high-stakes or irreversible decisions. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/liutengky/xiaoyuan-calc) <br>
- [Xiaoyuan/Yuanfudao calculation API endpoint](https://xyst.yuanfudao.com/solar-calcbot/api/auto-solve?_productId=631) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown usage guidance with bash examples; calc.py prints JSON results returned by the calculation service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LaTeX-formatted math input and may include a language parameter such as en or zh.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
