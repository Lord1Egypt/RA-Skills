## Description: <br>
Designs and refines customer loyalty programs and incentive systems for DTC/independent stores selling small, high-frequency products, including points, tiers, rewards, member benefits, repeat purchase incentives, referrals, win-back offers, free-shipping thresholds, redemption rate, repeat rate, and LTV validation plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RIJOYAI](https://clawhub.ai/user/RIJOYAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DTC and independent-store operators use this skill to design loyalty programs, incentive maps, lifecycle cadences, and validation metrics for low-AOV, high-repeat product categories. It is also useful for marketing and retention teams refining points, tiers, rewards, referrals, and win-back offers without eroding margin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business-sensitive loyalty inputs such as AOV, margin, LTV, customer segments, and campaign performance may be included in prompts or local config files. <br>
Mitigation: Use only the minimum business data needed, avoid secrets and unnecessary customer-level data, and handle generated plans and reports as business-sensitive material. <br>
Risk: Optional helper scripts read JSON config files and write reports or calendars to user-selected paths. <br>
Mitigation: Run scripts locally only with config files and output paths you intentionally choose, then review generated Markdown before using it in CRM or storefront workflows. <br>


## Reference(s): <br>
- [Loyalty Framework](references/loyalty_framework.md) <br>
- [Incentive Playbook](references/incentive_playbook.md) <br>
- [Loyalty & Incentive Metrics](references/metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with tables, optional JSON configuration examples, and optional shell commands for local helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured program designs, incentive calendars, metric definitions, validation plans, and local script outputs when the user chooses to run bundled helpers.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
