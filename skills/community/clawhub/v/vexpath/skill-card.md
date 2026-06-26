## Description: <br>
VexPath turns an OpenClaw instance into an operations assistant for email triage, inbox monitoring, lead classification, workflow automation, bottleneck audits, follow-up tracking, onboarding, content strategy, CRM sync, scheduling coordination, approval-based email drafting, and business operations analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smithbrock02-cmyk](https://clawhub.ai/user/smithbrock02-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, agencies, and service teams use this skill to triage email, draft approved replies, track follow-ups, design repeatable workflows, onboard clients, plan content, and identify operational bottlenecks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials and persistent inbox monitoring can expose sensitive business communications. <br>
Mitigation: Use OAuth or app passwords where possible, avoid passing passwords on the command line, restrict workspace file access, and install only the email features that are required. <br>
Risk: Approval-based email drafting and cold-outreach tooling can create unwanted or noncompliant outbound communication if misused. <br>
Mitigation: Keep outbound sending approval-only, review every draft before sending, and confirm consent, unsubscribe handling, and lawful basis for contacted leads. <br>
Risk: Roofing lead enrichment and estimation workflows process addresses and rely on external API calls. <br>
Mitigation: Remove or disable the roofing estimator and cold-outreach scripts unless they are explicitly needed, legally justified, and configured with protected API credentials. <br>
Risk: Workspace behavior files can change how an agent operates after they are copied into a client workspace. <br>
Mitigation: Review behavior files before copying them, keep human approval gates for important messages, and preserve logging and error handling in generated workflows. <br>


## Reference(s): <br>
- [VexPath Skill Page](https://clawhub.ai/smithbrock02-cmyk/vexpath) <br>
- [Email Triage Reference](references/email-triage.md) <br>
- [Onboarding Reference](references/onboarding.md) <br>
- [Follow-Up Tracking Reference](references/follow-up.md) <br>
- [Content Strategy Reference](references/content-strategy.md) <br>
- [Bottleneck Audit Reference](references/bottleneck-audit.md) <br>
- [Workflow Templates Reference](references/workflow-templates.md) <br>
- [Gmail Setup Reference](references/gmail-setup.md) <br>
- [Roofing Estimator Reference](references/roofing-estimator.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, structured triage summaries, JSON-like reports, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce email triage summaries, draft replies, workflow documentation, bottleneck audit reports, CRM update guidance, setup commands, and local configuration when the operator runs bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
