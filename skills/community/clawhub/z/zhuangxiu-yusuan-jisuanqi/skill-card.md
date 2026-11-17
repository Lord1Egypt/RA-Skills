## Description: <br>
装修预算计算器根据建筑面积、房屋新旧、半包或全包方式和装修档次，使用西安地区参考预算数据估算装修总价区间、分项费用和常见超预算风险。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zx029w](https://clawhub.ai/user/zx029w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External homeowners and renovation planning assistants use this skill to estimate rough renovation budgets from area, house condition, package type, and finish level. The estimates are calibrated to Xi'an reference pricing and are intended for planning, comparison, and quote-readiness rather than binding contractor pricing. <br>

### Deployment Geography for Use: <br>
China, with reference pricing calibrated for Xi'an; other cities require local labor and material price adjustment. <br>

## Known Risks and Mitigations: <br>
Risk: The reference material includes real Xi'an community names used as calibration examples. <br>
Mitigation: Do not reproduce internal calibration examples or specific community names in user-facing answers; generalize them as Xi'an reference cases. <br>
Risk: Users may mistake rough renovation estimates for a binding contractor quote. <br>
Mitigation: State that outputs are Xi'an reference estimates, not committed prices, and advise users to rely on formally signed contractor budget documents for final decisions. <br>


## Reference(s): <br>
- [标准预算结构](artifact/references/标准预算结构.md) <br>
- [西安地区装修参考价目表](artifact/references/西安参考价目表.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style Chinese text with budget ranges, line-item cost categories, boundary notes, and overrun warnings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Budget figures are rough estimates in ten-thousand-yuan units and exclude furniture, appliances, and soft furnishings unless otherwise stated.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
