## Description: <br>
Manage your Sensorpro email marketing account in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forcequit](https://clawhub.ai/user/forcequit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure access to Sensorpro and manage contacts, campaigns, metrics, relay email, imports, and account actions through documented Sensorpro API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live email and campaign actions can send or broadcast messages to real recipients. <br>
Mitigation: Require explicit confirmation of recipients, payloads, lists, campaign IDs, and send timing before any send or broadcast action. <br>
Risk: Deletion, import, opt-out, and account-user changes can alter customer or account data. <br>
Mitigation: Use a dedicated least-privilege API user and verify affected lists, contact IDs, import targets, and account-user changes before executing mutating API calls. <br>
Risk: The skill depends on Sensorpro API credentials stored in environment variables. <br>
Mitigation: Store credentials in a protected .env or process manager, avoid committing secrets, and rotate the API key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/forcequit/sensorpro) <br>
- [OpenClaw Sensorpro homepage](https://github.com/forcequit/openclaw-sensorpro) <br>
- [Sensorpro API documentation](https://sensorpro.net/api/) <br>
- [Sensorpro Contacts API](https://sensorpro.net/api/contacts.html) <br>
- [Sensorpro Campaigns and metrics API](https://sensorpro.net/api/campaigns.html) <br>
- [Sensorpro Relay Email API](https://sensorpro.net/api/sendemail.html) <br>
- [Sensorpro Imports API](https://www.sensorpro.net/api/imports.html) <br>
- [Sensorpro Account API](https://sensorpro.net/api/account.html) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Sensorpro credentials and curl/python3 availability.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
