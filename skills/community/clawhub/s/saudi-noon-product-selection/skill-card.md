## Description: <br>
沙特 Noon 电商选品工具。分析指定市场的竞争情况，识别蓝海产品。触发条件：用户要求选品、分析市场、查找蓝海产品。完整流程：市场翻译 -> Noon 商品搜索 -> 语义分析卖点 -> 供给量搜索 -> 蓝海识别 -> 定价建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freemanwangfuhan-coder](https://clawhub.ai/user/freemanwangfuhan-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and marketplace researchers use this skill to research Saudi Noon product categories, compare visible supply signals, identify lower-competition product opportunities, and produce pricing suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependent skills may add behavior or data handling that is not covered by this skill's clean security verdict. <br>
Mitigation: Review zh-to-ar-translator, noon-product-search, and noon-product-count separately before deployment. <br>
Risk: Generic market-analysis prompts may activate this Noon-focused workflow when a different marketplace or region was intended. <br>
Mitigation: Specify the intended marketplace and region in user requests, and confirm the workflow scope before running searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freemanwangfuhan-coder/saudi-noon-product-selection) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes market overview, product type analysis, selling-point supply counts, price bands, blue-ocean opportunity assessment, and pricing suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
