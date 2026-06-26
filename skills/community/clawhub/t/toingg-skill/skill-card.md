## Description: <br>
Automate Toingg ops by creating campaigns, scheduling daily analytics, converting Excel contacts, uploading lists, and sending WhatsApp template messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinavpgagi](https://clawhub.ai/user/abhinavpgagi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Toingg campaign workflows from an agent, including campaign creation, analytics pulls, contact-list preparation, contact uploads, and WhatsApp template sends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Toingg account through campaign, contact upload, WhatsApp template, analytics, and cron workflows. <br>
Mitigation: Install it only when Toingg account automation is intended, and use the least-privileged Toingg token available. <br>
Risk: Contact exports, recipient lists, campaign payloads, and analytics snapshots may contain personal or campaign data. <br>
Mitigation: Review payloads and recipient lists before running scripts, upload only contacts authorized for messaging, and avoid committing exports or analytics to broadly shared storage. <br>
Risk: The optional analytics cron performs daily background pulls when enabled. <br>
Mitigation: Enable the cron only after explicit user confirmation, confirm the output directory, and document how to disable the scheduled job. <br>


## Reference(s): <br>
- [Analytics Cron Playbook](references/analytics-cron.md) <br>
- [Contact Upload + WhatsApp Template Workflow](references/contact-workflow.md) <br>
- [Toingg Campaign Payload Template](references/payload-template.md) <br>
- [Toingg add_contacts API endpoint](https://prepodapi.toingg.com/api/v3/add_contacts) <br>
- [Toingg create_campaign API endpoint](https://prepodapi.toingg.com/api/v3/create_campaign) <br>
- [Toingg get_campaign_analytics API endpoint](https://prepodapi.toingg.com/api/v3/get_campaign_analytics) <br>
- [Toingg send_whatsapp_templates API endpoint](https://prepodapi.toingg.com/api/v3/send_whatsapp_templates) <br>
- [ClawHub skill page](https://clawhub.ai/abhinavpgagi/toingg-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON payloads, and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Toingg API responses, campaign payload files, contact JSON exports, analytics JSON snapshots, and cron setup commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
