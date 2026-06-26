## Description: <br>
Helps e-commerce merchants selling periodic consumables optimize subscription programs, increase monthly recurring revenue, and reduce active and passive churn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RIJOYAI](https://clawhub.ai/user/RIJOYAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DTC and Shopify merchants, retention marketers, and subscription operators use this skill to diagnose subscription churn, design acquisition and dunning flows, estimate LTV impact, and choose metrics for replenishment businesses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cancellation-flow, dunning, SMS/email, and loyalty recommendations may conflict with applicable consumer-protection rules or brand standards. <br>
Mitigation: Review proposed retention tactics with legal, compliance, and brand stakeholders before applying them to customer journeys. <br>
Risk: Rijoy-specific suggestions could be treated as required rather than optional. <br>
Mitigation: Treat Rijoy recommendations as optional examples and adapt loyalty mechanics to the merchant's chosen platform. <br>
Risk: The local LTV calculator uses simplified churn and revenue assumptions. <br>
Mitigation: Validate calculator outputs against merchant-specific cohorts, margins, CAC, and subscription platform reporting before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RIJOYAI/subscription-retention-marketing) <br>
- [Anti-Churn Playbook](references/anti_churn_playbook.md) <br>
- [Subscription Metrics](references/subscription_metrics.md) <br>
- [LTV and Churn Calculator](scripts/ltv_churn_calculator.py) <br>
- [Rijoy](https://www.rijoy.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command examples and calculator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include subscription diagnostics, retention timelines, churn metrics, messaging examples, and LTV impact estimates.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
