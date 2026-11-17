## Description: <br>
轻量工作流 helps agents guide users through a quick automation-worthiness check, three minimal workflow templates, and a one-page automation cheat sheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and nontechnical teams use this skill to decide whether a repetitive task is worth automating and to draft a minimal no-code workflow for forms, payments, invoices, scheduled reports, or notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Beginners may apply payment, invoicing, or customer-message workflow templates directly to live business systems. <br>
Mitigation: Test first with sandbox Stripe, accounting, and email accounts, and require human approval before invoices or customer emails go live. <br>
Risk: The skill declares broad command capability without a documented command-running use case. <br>
Mitigation: Remove exec permission unless a concrete command-running use case is added and reviewed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with scoring tables, workflow templates, checklists, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tool-specific setup guidance for Zapier, Make, n8n, Stripe, accounting tools, email, or Slack.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
