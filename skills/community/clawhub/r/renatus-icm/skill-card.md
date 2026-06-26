## Description: <br>
Manage Renatus event marketing campaigns as an ICM, including event registration campaigns, commercial email blasts, event landing pages, Supabase lead exports, unsubscribe sync, and browser-based guest registration via CDP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Renatus ICM users and campaign operators use this skill to set up event pages, send commercial email campaigns, register guests, export lead data, and sync unsubscribes across Renatus and Supabase workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse live browser sessions through CDP. <br>
Mitigation: Use a dedicated low-privilege browser profile and do not expose a main browser profile over CDP. <br>
Risk: The skill can export and store lead data and campaign logs. <br>
Mitigation: Keep lead exports and logs private, use least-privilege Renatus and Supabase credentials, and avoid production service-role keys unless strictly necessary. <br>
Risk: The skill can send bulk commercial email and delete records. <br>
Mitigation: Run dry runs before sending or deleting, review batch inputs before execution, and keep destructive actions gated by explicit execution flags. <br>
Risk: The unsubscribe cron workflow can remove records on a schedule. <br>
Mitigation: Do not enable the cron workflow until the backend unsubscribe flow and deletion safeguards are verified. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/earlvanze/renatus-icm) <br>
- [Renatus ICM Workflows](references/workflows.md) <br>
- [Email Campaign Guide](references/email-campaign.md) <br>
- [Event Page Setup Guide](references/event-page-setup.md) <br>
- [Supabase Setup for Renatus ICM](references/supabase-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, configuration steps, generated HTML/email assets, CSV/JSON lead exports, and operational scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send bulk email, access browser session tokens through local CDP, export lead data, and delete records when execution flags and credentials are supplied.] <br>

## Skill Version(s): <br>
2.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
