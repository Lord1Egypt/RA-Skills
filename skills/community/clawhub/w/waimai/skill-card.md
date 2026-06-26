## Description: <br>
Waimai takeout decision assistant. Input cuisine, budget, location constraints, merchant candidates, or a takeout link; compare delivery fee, minimum order, discounts, meal fit, timing, and merchant risk. Safe boundary: no login, no order submission, no payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compare public takeout options by cost, delivery timing, promotion fit, meal suitability, and merchant risk before placing an order themselves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may treat public takeout comparison guidance as permission to share credentials, addresses, SMS codes, payment details, or checkout authority. <br>
Mitigation: Keep use limited to advisory comparison of public or user-provided information; do not enter sensitive data or place orders through the skill. <br>
Risk: Prices, delivery times, coupons, merchant terms, and availability can change before checkout. <br>
Mitigation: Have the user verify final price, delivery time, coupons, merchant terms, and order details in the ordering app before paying. <br>
Risk: Promotions such as minimum-order discounts or bundles may appear attractive while producing poor real checkout fit. <br>
Mitigation: Compare delivery fee, minimum order, delivery time, promotions, scenario fit, and merchant risk together rather than choosing by headline discount. <br>


## Reference(s): <br>
- [Comparison Guide](references/comparison-guide.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Risk Signals](references/risk-signals.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with sections for best option, reasons, caveats, and final advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No account access, checkout action, payment action, browser automation, or data persistence is performed by the skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
