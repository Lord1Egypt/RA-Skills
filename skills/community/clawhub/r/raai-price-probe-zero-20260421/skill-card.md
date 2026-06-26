## Description: <br>
AI-Поддержка PRO is a Russian-language customer-support automation skill for ticket categorization, SLA tracking, L1/L2/L3 escalation, sentiment analysis, response drafting, NPS/CSAT reporting, operator onboarding, and CRM-assisted support workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support leads, operators, and business owners use this skill to standardize high-volume customer-support operations: categorize incoming tickets, monitor SLA risk, route escalations, draft customer responses, prepare support reports, and guide operator onboarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release name and package metadata are inconsistent with the AI-Поддержка PRO customer-support behavior. <br>
Mitigation: Confirm this is the intended customer-support automation skill before installation or deployment. <br>
Risk: The skill can affect customer data, CRM records, customer replies, and refunds without enough control guidance. <br>
Mitigation: Disable CRM writes, auto-refunds, and customer-facing sends until explicit approval gates are configured and tested. <br>
Risk: The skill requires sensitive API, CRM, and Telegram credentials. <br>
Mitigation: Use least-privilege credentials and configure redaction, retention, and escalation-channel rules before operational use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raaipro/raai-price-probe-zero-20260421) <br>
- [Publisher profile](https://clawhub.ai/user/raaipro) <br>
- [README](artifact/README.md) <br>
- [Quick start examples](artifact/examples/quick-start.md) <br>
- [Onboarding guide](artifact/docs/onboarding.md) <br>
- [Anti-fail guide](artifact/docs/anti-fail.md) <br>
- [ROI guide](artifact/docs/roi.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, structured support reports, response templates, checklists, and shell-command setup snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configuration for company support policy, SLA matrix, escalation owners, CRM/API credentials, and approval gates before operational use.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
