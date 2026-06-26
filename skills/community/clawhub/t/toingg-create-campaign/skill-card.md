## Description: <br>
End-to-end Toingg operations toolkit for creating campaigns, discovering campaign IDs, placing calls, scheduling analytics pulls, uploading contacts, and sending WhatsApp template outreach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinavpgagi](https://clawhub.ai/user/abhinavpgagi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to automate Toingg voice and WhatsApp campaign workflows, including campaign creation, campaign lookup, on-demand calls, analytics pulls, contact upload, and template sends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Toingg account to place calls, upload contacts, and send WhatsApp templates, which could contact unintended or non-consenting recipients. <br>
Mitigation: Before running outreach actions, confirm recipient consent, lawful basis, phone numbers, approved template and locale, and opt-out handling. <br>
Risk: Toingg API tokens, contact exports, and API response files may expose account access or personal data. <br>
Mitigation: Keep TOINGG_API_TOKEN private and scoped, and avoid committing contact exports or API responses that contain personal data. <br>
Risk: The optional analytics cron can create scheduled background pulls from the Toingg account. <br>
Mitigation: Enable the cron only after explicit user confirmation, verify the intended schedule and output path, and document how to disable it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhinavpgagi/toingg-create-campaign) <br>
- [Analytics Cron Playbook](references/analytics-cron.md) <br>
- [Contact Upload + WhatsApp Template Workflow](references/contact-workflow.md) <br>
- [Toingg Campaign Payload Template](references/payload-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads or API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce campaign payloads, contact JSON, analytics snapshots, and API response logs when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
