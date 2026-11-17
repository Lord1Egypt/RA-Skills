## Description:

Send and close SIGNL4 alerts using the SIGNL4 inbound webhook with a SIGNL4 team secret.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rons4](https://clawhub.ai/user/rons4)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to generate curl-based SIGNL4 webhook requests that create alerts and resolve existing alerts by external correlation ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SIGNL4 team secret is embedded in the webhook URL and could be exposed if printed, logged, or sent to an untrusted endpoint.

Mitigation: Treat SIGNL4_TEAM_SECRET as confidential and keep SIGNL4_WEBHOOK_BASE fixed to the official SIGNL4 endpoint unless a trusted proxy is deliberately used.

Risk: Alert titles, messages, and optional fields are inserted into curl JSON templates and may break JSON or change the request if unsanitized text is used.

Mitigation: Build payloads with a JSON serializer such as jq and validate user-provided alert fields before execution.

Risk: Resolving an alert depends on reusing the same external correlation ID that created the alert.

Mitigation: Record and confirm X-S4-ExternalID values before sending close requests.

## Reference(s):

- [SIGNL4 webhook documentation](https://docs.signl4.com/integrations/webhook/webhook.html)
- [SIGNL4 product information](https://www.signl4.com/)
- [ClawHub skill page](https://clawhub.ai/rons4/skills/signl4)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and webhook field guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl templates and requires SIGNL4_TEAM_SECRET; SIGNL4_WEBHOOK_BASE is optional.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
