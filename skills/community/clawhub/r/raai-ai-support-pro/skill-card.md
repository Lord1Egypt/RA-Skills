## Description: <br>
Ai Support Pro helps customer-support teams classify tickets, track SLA risk, route escalations across L1/L2/L3, draft customer responses, review sentiment, prepare NPS/CSAT reports, onboard operators, and configure CRM-connected support workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer-support leaders, operators, and operations teams use this skill to standardize ticket intake, SLA tracking, escalation decisions, customer-response drafting, CRM-card summaries, and support-quality reporting for businesses with recurring support volume. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process customer records and CRM context. <br>
Mitigation: Use least-privilege CRM credentials, limit access to required fields, and test with sample or redacted customer records before connecting production data. <br>
Risk: The skill can draft or trigger customer-facing messages and ticket closures. <br>
Mitigation: Require human approval before sending messages, closing tickets, or updating customer records until support policies and escalation rules are validated. <br>
Risk: Refund and compensation workflows can affect customer finances or commitments. <br>
Mitigation: Disable refund automation or keep it in dry-run mode until return policies, approval thresholds, and manager review steps are confirmed. <br>
Risk: SLA and escalation outputs depend on accurate ticket data, assigned owners, and configured policies. <br>
Mitigation: Populate SLA targets, L2/L3 owners, ticket categories, and CRM fields before operational use, then review daily reports during rollout. <br>
Risk: The artifact includes install and build scripts. <br>
Mitigation: Review scripts before execution and run smoke tests in a sandbox before granting production credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raaipro/raai-ai-support-pro) <br>
- [Publisher profile](https://clawhub.ai/user/raaipro) <br>
- [README](artifact/README.md) <br>
- [Configuration reference](artifact/config.yaml) <br>
- [Onboarding guide](artifact/docs/onboarding.md) <br>
- [Limitations and anti-fail guidance](artifact/docs/anti-fail.md) <br>
- [Quick-start examples](artifact/examples/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured operational text with configuration snippets and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ticket classifications, SLA reports, escalation briefs, customer-response drafts, CRM-card summaries, onboarding checklists, and support analytics guidance.] <br>

## Skill Version(s): <br>
3.5.2 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
