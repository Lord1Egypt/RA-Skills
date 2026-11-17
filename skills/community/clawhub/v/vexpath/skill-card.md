## Description:

VexPath turns an OpenClaw instance into an operations assistant for email triage, inbox monitoring, lead classification, workflow automation, bottleneck audits, follow-up tracking, client onboarding, content strategy, CRM sync, scheduling coordination, approval-based email drafting, and business operations analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smithbrock02-cmyk](https://clawhub.ai/user/smithbrock02-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators, agencies, service teams, and their agents use VexPath to triage email, classify leads, draft approved replies, track follow-ups, document workflows, audit bottlenecks, and coordinate CRM or calendar updates. The skill is aimed at repeatable business operations support rather than autonomous unsupervised messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad mailbox, calendar, CRM, and memory-file access for triage, scheduling, follow-up tracking, and heartbeat checks.

Mitigation: Grant only the accounts and folders needed for the deployment, review access scopes before enabling monitoring, and confirm retention for follow-up and daily log files.

Risk: Email setup examples and scripts accept mailbox passwords or app passwords and may store them in local configuration.

Mitigation: Use OAuth, a keychain, or a password manager where possible; avoid placing mailbox passwords in command history or chat; restrict local config permissions and rotate exposed credentials.

Risk: The VPS provisioning path uses remote shell installation patterns and installs system or npm dependencies.

Mitigation: Do not run curl-to-bash provisioning directly; inspect scripts first, pin dependency versions, and execute deployment steps manually in a controlled environment.

Risk: The SOUL.md and HEARTBEAT.md assets establish persistent operating behavior and periodic monitoring instructions.

Mitigation: Deploy those files only when persistent VEX behavior is desired, review the heartbeat checklist, and disable or narrow checks that are outside the intended business workflow.

Risk: The skill drafts outbound emails, follow-ups, outreach, estimates, and scheduling responses that could affect customers or prospects.

Mitigation: Keep human approval gates enabled for important outbound communication and verify estimates, legal or payment-related messages, and customer-facing drafts before sending.

## Reference(s):

- [Bottleneck Audit Reference](references/bottleneck-audit.md)
- [Content Strategy Reference](references/content-strategy.md)
- [Email Triage Reference](references/email-triage.md)
- [Follow-Up Tracking Reference](references/follow-up.md)
- [Gmail Setup Guide](references/gmail-setup.md)
- [Client Onboarding Reference](references/onboarding.md)
- [VexPath Roofing Contractor Automation Module](references/roofing-estimator.md)
- [Workflow Templates Reference](references/workflow-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON triage reports, CSV templates, shell scripts, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows create local configuration, memory, report, or CRM files and require human approval before sending important outbound messages unless explicitly permitted.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
