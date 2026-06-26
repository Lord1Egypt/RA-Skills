## Description: <br>
购物助手 helps agents provide coupon lookup, multi-platform price comparison, price protection, price history, and price-drop reminder guidance for Taobao/Tmall, JD, and Pinduoduo shopping links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaichao87](https://clawhub.ai/user/wuhaichao87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping-focused agents use this skill to inspect product links, find coupons, compare prices across supported Chinese e-commerce platforms, and produce purchase guidance. It is suited to shopping assistance workflows where current prices, coupon availability, and platform-specific limitations need to be shown clearly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping links may be converted into affiliate or tracking links without clear user-facing consent. <br>
Mitigation: Review the skill before installation and disclose or disable affiliate conversion where users require direct destination links. <br>
Risk: Affiliate and commerce API credentials may grant access beyond the skill's shopping-assistance workflow. <br>
Mitigation: Use dedicated low-privilege credentials for Zhetaoke, JD Union, and Taobao Union integrations, and rotate them if exposed. <br>
Risk: The artifact references helper scripts that are not included in the submitted files. <br>
Mitigation: Do not run referenced helper scripts unless their source is included, reviewed, and scanned in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wuhaichao87/shopping-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/wuhaichao87) <br>
- [Taobao](https://www.taobao.com) <br>
- [JD.com](https://www.jd.com) <br>
- [Pinduoduo](https://www.pinduoduo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured shopping results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include coupon links, price comparisons, price-protection guidance, historical price notes, and purchase recommendations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
