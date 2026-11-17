## Description:

Manage Renatus event marketing campaigns as an ICM, including event registration campaigns, commercial email blasts, event landing pages, Supabase lead exports, unsubscribe syncing, and browser-based guest registration via CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Independent campaign managers and supporting operators use this skill to set up Renatus event pages, send campaign email, register guests, export leads, and process unsubscribes across Renatus, Supabase, and local campaign assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate as a privileged campaign-admin tool that handles browser session tokens, Renatus credentials, Supabase tokens, lead exports, and email-sending accounts.

Mitigation: Use a dedicated browser profile for CDP, avoid production service-role keys, prefer least-privilege tokens, and rotate credentials after use or exposure.

Risk: Lead deletion, unsubscribe automation, mass email, and guest registration can affect real contacts and compliance obligations.

Mitigation: Run dry-run or test flows first, verify consent and unsubscribe handling before sending email, and review campaign logs before broad execution.

Risk: The security summary notes unsafe or incomplete controls around admin exports, scheduled unsubscribe automation, and missing or unaudited Supabase functions.

Mitigation: Review or replace the unsubscribe workflow, do not deploy missing or unaudited Supabase functions, and validate admin export controls in a dedicated test project.

## Reference(s):

- [Renatus ICM Workflows](artifact/references/workflows.md)
- [Email Campaign Guide](artifact/references/email-campaign.md)
- [Event Page Setup Guide](artifact/references/event-page-setup.md)
- [Supabase Setup for Renatus ICM](artifact/references/supabase-setup.md)
- [Renatus Back Office Order Entry API](artifact/references/order-entry-backoffice-api.md)
- [ClawHub skill release page](https://clawhub.ai/earlvanze/skills/renatus-icm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, generated HTML files, and CSV or JSON lead-export artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on privileged browser sessions, Renatus credentials, Supabase tokens, SMTP or gws access, and local campaign configuration.]

## Skill Version(s):

2.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
