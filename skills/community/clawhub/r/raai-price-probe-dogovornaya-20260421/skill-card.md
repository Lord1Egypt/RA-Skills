## Description: <br>
AI customer-support skill that helps categorize tickets, track SLA status, route escalations, draft replies, and summarize support metrics for Russian-language support teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support leaders, operators, and implementation teams use this skill to standardize customer-support workflows across ticket categorization, SLA monitoring, escalation, response drafting, CRM context review, refunds, and quality reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad authority over customer messages, CRM context, and refund-related workflows without enough scoping or approval controls. <br>
Mitigation: Use it only in a clearly selected support workflow, narrow triggers and credentials, and require human approval before refunds or CRM updates. <br>
Risk: Support workflows may expose customer identifiers, contact details, order data, lifetime value, payment or refund details, and complaint history. <br>
Mitigation: Add privacy rules that minimize access to sensitive customer data and restrict storage, sharing, and display to what each support task requires. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raaipro/raai-price-probe-dogovornaya-20260421) <br>
- [README](README.md) <br>
- [Onboarding guide](docs/onboarding.md) <br>
- [Anti-fail guide](docs/anti-fail.md) <br>
- [Quick start examples](examples/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured ticket summaries, support reports, reply templates, configuration guidance, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Customer-facing replies, refunds, CRM updates, and escalations should be reviewed by a human before execution.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
