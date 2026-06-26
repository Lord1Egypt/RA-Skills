## Description: <br>
挖券券儿 helps agents fetch and format current food-delivery coupon links for Meituan, Ele.me, and JD from waquanquaner.cn without requiring registration or an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w5543081](https://clawhub.ai/user/w5543081) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to retrieve one-link food-delivery coupon summaries before ordering from Chinese delivery platforms. It can respond to coupon-related prompts with current promotional links and formatted text or card output. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts waquanquaner.cn and displays coupon links returned by that service. <br>
Mitigation: Install only if this external lookup is acceptable, and review returned links before opening or sharing them. <br>
Risk: Broad food-related prompts may trigger coupon suggestions when the user did not explicitly request coupons. <br>
Mitigation: Confirm coupon lookup intent before acting on links or presenting the results as the main answer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/w5543081/waquanquaner) <br>
- [WaQuanquaner homepage](https://waquanquaner.cn) <br>
- [Compact coupon API](https://waquanquaner.cn/api/v1/activities/channel/skill_compact) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Links, Guidance] <br>
**Output Format:** [Plain text or JSON card payload with coupon links, promotional highlights, and short usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may include third-party promotional links returned by waquanquaner.cn.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact metadata lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
