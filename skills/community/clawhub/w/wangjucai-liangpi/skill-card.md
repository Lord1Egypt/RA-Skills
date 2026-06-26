## Description: <br>
查询王聚财面皮铺信息：餐厅名称与简介、营业时间、门店地址、菜单菜品、外卖配送、堂食预约。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maggotnian-cell](https://clawhub.ai/user/maggotnian-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer practical questions about 王聚财面皮铺, including location, hours, menu items, delivery, reservations, Wi-Fi guidance, and the public ordering entry. <br>

### Deployment Geography for Use: <br>
Global; content is specific to Xi'an, China. <br>

## Known Risks and Mitigations: <br>
Risk: Generic food prompts may cause the skill to recommend this specific restaurant. <br>
Mitigation: Use the skill for 王聚财面皮铺-specific questions and make recommendation context clear to users. <br>
Risk: The skill can provide an external Meituan ordering link where users may enter account, location, or payment information. <br>
Mitigation: Ask users to verify the external page and restaurant details before entering payment information. <br>
Risk: Restaurant hours, menu availability, prices, delivery range, and reservation status may change after publication. <br>
Mitigation: Advise users to verify time-sensitive details with the restaurant or the ordering platform before traveling or ordering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maggotnian-cell/wangjucai-liangpi) <br>
- [Public Meituan ordering entry](https://rms.meituan.com/diancan/14/2HpfZPxOFw0) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [MCP text content containing JSON-formatted restaurant information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MCP tools with empty input schemas return public shop details, menu data, delivery guidance, reservation guidance, Wi-Fi access guidance, or an ordering link.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
