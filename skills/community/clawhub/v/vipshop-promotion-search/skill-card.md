## Description: <br>
查询唯品会促销活动，汇总活动状态、类型、时间、品牌、链接和活动图片，供用户了解当前或近期优惠专场。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viphgta](https://clawhub.ai/user/viphgta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to retrieve and summarize Vipshop promotion activity, including active and upcoming campaigns, participating brands, activity links, and banner images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start a Vipshop login flow and use a stored account session token. <br>
Mitigation: Require explicit user confirmation before login, dependency installation, or any query that uses the user's account token. <br>
Risk: The skill may install or run the separate vipshop-user-login dependency. <br>
Mitigation: Review the dependency before installation and restrict use to Vipshop promotion requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/viphgta/vipshop-promotion-search) <br>
- [Vipshop promotion API endpoint](https://api.union.vip.com/vsp/common/getActListForAI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown summary with JSON data from the promotion query script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes grouped activity counts, active and upcoming activity lists, activity links, and banner image URLs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
