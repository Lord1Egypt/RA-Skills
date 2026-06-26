## Description: <br>
A Russian-language customer support automation skill for categorizing tickets, tracking SLA, routing escalations, drafting customer replies, producing support reports, and guiding CRM-backed support workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support leaders, operations managers, and support teams use this skill to standardize ticket triage, escalation, SLA monitoring, response drafting, onboarding, and daily support reporting for businesses with recurring customer requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process customer data and produce CRM updates or customer messages without clear privacy and approval boundaries. <br>
Mitigation: Start with test data and least-privilege credentials; configure redaction, retention, and human approval before using live customer records or sending outbound messages. <br>
Risk: Refund, compensation, escalation, and customer-response workflows could affect customers or business operations if automated without review. <br>
Mitigation: Disable automatic CRM writes, refunds, compensation decisions, and outbound customer messages until an accountable human approval flow is configured. <br>
Risk: The packaged install flow references a .env.example file that is not present in the artifact evidence. <br>
Mitigation: Fix the setup package or provide the missing environment template before installation, and verify required API keys and optional integration credentials are documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raaipro/raai-price-probe-noprice-20260421) <br>
- [README](README.md) <br>
- [Onboarding guide](docs/onboarding.md) <br>
- [Anti-fail guide](docs/anti-fail.md) <br>
- [ROI guide](docs/roi.md) <br>
- [Quick start examples](examples/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration snippets, shell commands, ticket summaries, escalation notes, customer response templates, and operational reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily Russian-language support operations content; may reference customer records, CRM fields, refund workflows, SLA status, and outbound customer messaging.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
