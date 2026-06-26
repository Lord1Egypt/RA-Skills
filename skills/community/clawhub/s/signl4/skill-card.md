## Description: <br>
Send and close SIGNL4 alerts using the SIGNL4 inbound webhook with the team secret in the URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rons4](https://clawhub.ai/user/rons4) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and incident-response teams use this skill to send SIGNL4 alerts and resolve existing alerts by external correlation ID from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SIGNL4 team secret is embedded in the webhook URL and could authorize alert operations if exposed. <br>
Mitigation: Store SIGNL4_TEAM_SECRET in a protected environment or secrets manager, avoid printing it in responses or logs, and rotate it if exposure is suspected. <br>
Risk: Alert titles, messages, external IDs, service names, scenario values, and location data are sent to SIGNL4. <br>
Mitigation: Confirm this data sharing is acceptable for the deployment environment and avoid placing regulated or unnecessary sensitive data in alert bodies. <br>


## Reference(s): <br>
- [SIGNL4 Webhook Documentation](https://docs.signl4.com/integrations/webhook/webhook.html) <br>
- [SIGNL4 Product Information](https://www.signl4.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/rons4/signl4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown with inline shell command examples and status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SIGNL4_TEAM_SECRET; SIGNL4_WEBHOOK_BASE is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
