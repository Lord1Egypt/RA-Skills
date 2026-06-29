## Description: <br>
信创与 IT 信息化采招数据分析助手，用于检索招中标公告、分析 IT 品牌与型号价格、识别采购单位和供应商、评估集成商竞争格局，并支持数字政府与国产化选型情报分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement analysts, IT vendors, system integrators, and agents use this skill to query Chinese Xinchuang and IT procurement data, compare brands and prices, find purchasers and suppliers, and support digital government localization sourcing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic registration fingerprints the user's device and sends device and user identifiers to the vendor when no API key is configured. <br>
Mitigation: Prefer a manually configured ZLBX_API_KEY or require explicit organizational approval before allowing automatic registration. <br>
Risk: The skill can persist an API key in ~/.zlbx/config.json and generate auto-login recharge links. <br>
Mitigation: Review local credential storage and recharge-link handling against organizational security policy before use. <br>
Risk: Contact lookup and broad IT-procurement triggers may involve sensitive procurement or contact data. <br>
Mitigation: Confirm the skill's scope matches privacy and procurement-data policies before enabling broad use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiliaobiaoxun/skills/xinchuang-it-procurement-analyzer) <br>
- [API search reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance, configuration] <br>
**Output Format:** [Markdown text with JSON request examples and structured procurement analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use ZLBX_API_KEY or a local ~/.zlbx/config.json API key; automatic registration can create and persist an account key when no key is configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
