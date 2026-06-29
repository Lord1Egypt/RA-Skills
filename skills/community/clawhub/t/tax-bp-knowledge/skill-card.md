## Description: <br>
税务BP客服知识库 helps an agent answer Meituan tax-support questions by routing business-line context, retrieving Sankuai KM tax documents, and using web search only when internal knowledge is missing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linweibin6992-blip](https://clawhub.ai/user/linweibin6992-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Tax BP support agents and internal business users use this skill to answer VAT, income tax, stamp tax, invoicing, settlement, and business-line tax questions for Meituan CLC delivery and in-store travel scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves internal Sankuai tax knowledge documents that may not be appropriate for every user. <br>
Mitigation: Confirm that the user is authorized to access the listed internal KM documents before retrieving or quoting them. <br>
Risk: Tax-support answers can be mistaken for final legal or tax advice. <br>
Mitigation: Present answers as support guidance, cite sources, and direct uncertain or high-impact questions to tax BP confirmation. <br>
Risk: Fallback web searches may return stale or non-authoritative policy sources. <br>
Mitigation: Prefer official tax authority source links and do not invent tax rates, policy document numbers, or interpretations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linweibin6992-blip/tax-bp-knowledge) <br>
- [Sankuai KM common tax FAQ](https://km.sankuai.com/collabpage/2769947356) <br>
- [Sankuai KM delivery tax FAQ](https://km.sankuai.com/collabpage/2769388613) <br>
- [Sankuai KM hotel and travel tax FAQ](https://km.sankuai.com/collabpage/2769258846) <br>
- [Sankuai KM common tax rules](https://km.sankuai.com/collabpage/2770026936) <br>
- [Sankuai KM delivery tax rules](https://km.sankuai.com/collabpage/2769787851) <br>
- [Sankuai KM hotel and travel tax rules](https://km.sankuai.com/collabpage/2769697987) <br>
- [Sankuai KM settlement and invoicing process](https://km.sankuai.com/collabpage/2769847682) <br>
- [Sankuai KM BP entry template](https://km.sankuai.com/collabpage/2769937421) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown answers with source links and occasional shell commands for retrieving internal documents or policy sources] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should cite the relevant KM document or official policy source, avoid unsupported tax rates or policy numbers, and defer uncertain issues to tax BP.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
