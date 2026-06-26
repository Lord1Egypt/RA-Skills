## Description: <br>
Wa Quanquaner helps agents find and present current food-delivery coupon and discount activity for Meituan, Ele.me, and JD in Mainland China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w5543081](https://clawhub.ai/user/w5543081) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in Mainland China use this skill to ask an agent for current food-delivery coupons and receive a concise link and activity summary for Meituan, Ele.me, or JD. <br>

### Deployment Geography for Use: <br>
China (Mainland) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate on broad food or meal-choice phrases and may surface coupon links when the user did not explicitly ask for discounts. <br>
Mitigation: Use or configure the skill for explicit coupon, discount, or food-delivery savings requests. <br>
Risk: The release requests broader shell permissions than a coupon lookup normally needs. <br>
Mitigation: Review requested permissions before installation and remove unrestricted PowerShell access unless it is required in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/w5543081/wa-quanquaner-skill) <br>
- [Publisher profile](https://clawhub.ai/user/w5543081) <br>
- [Wa Quanquaner activity API](https://waquanquaner.cn/api/v1/activities/channel/skill_compact) <br>
- [Wa Quanquaner coupon landing page](https://waquanquaner.cn/go) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain text or Markdown-style chat output, with optional Feishu card JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches current HTTPS activity data and renders coupon links and highlights; supports prompts focused on Meituan, Ele.me, and JD.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
