## Description: <br>
Helps compare takeout and food prices and coupons across Meituan, Ele.me, JD, Taobao, and related platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Consumers and shopping assistants use this skill to search multiple delivery and ecommerce platforms, compare estimated food or grocery prices, and identify available coupons before ordering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search-based prices, delivery fees, and coupons can be stale or vary by location, time, store, and user eligibility. <br>
Mitigation: Confirm final totals and coupon terms in the relevant platform apps before purchasing. <br>
Risk: The generated HTML report may load chart code from a CDN. <br>
Mitigation: Open reports in a trusted environment, or review and replace the CDN dependency when offline or controlled execution is required. <br>
Risk: The skill may activate on broad price-checking requests. <br>
Mitigation: Confirm the product, city, and whether the user wants price comparison, coupons, or both before running searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/waimai-compare) <br>
- [Publisher profile](https://clawhub.ai/user/bettermen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with structured JSON inputs and a generated local HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The HTML report may load chart code from a CDN and should be treated as a local report for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
