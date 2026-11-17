## Description:

Automates customer support workflows with SupportForge API examples for API key signup, ticket routing, response generation, knowledge-base search, sentiment analysis, workflow creation, integrations, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

Developers and support operations teams use this skill to call SupportForge endpoints for help desk automation, including ticket classification, routing, response drafting, knowledge-base lookup, escalation support, and analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer support prompts and examples may include personal data, account value, interaction history, or confidential business details sent to SupportForge.

Mitigation: Use the skill only when SupportForge is approved for the data being processed, and remove or minimize PII, regulated data, and confidential details before sending requests.

Risk: The skill includes commands that create and use API keys for a third-party service.

Mitigation: Store API keys securely, avoid committing them to files or chat transcripts, and rotate keys if they are exposed.

Risk: Automated response, routing, and escalation recommendations can be inaccurate or inappropriate for customer-facing support decisions.

Mitigation: Review generated responses and routing decisions before customer delivery or escalation, especially for billing, refunds, high-value accounts, and sensitive issues.

## Reference(s):

- [SupportForge API key endpoint](https://supportforge.vosscg.com/v1/keys)
- [SupportForge ticket routing endpoint](https://supportforge.vosscg.com/v1/tickets/route)
- [SupportForge response generation endpoint](https://supportforge.vosscg.com/v1/responses/generate)
- [SupportForge knowledge-base search endpoint](https://supportforge.vosscg.com/v1/kb/search)
- [SupportForge plans and upgrades](https://vosscg.com/forges)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown with inline curl commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SupportForge API key and may transmit customer support data to a third-party API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
