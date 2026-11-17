## Description:

Generates customized incident response playbooks tailored to organizational assessment data and security requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security operations centers, incident response teams, compliance officers, and security architects use this skill to generate organization-specific incident response playbooks from assessment data, risk context, compliance frameworks, and threat profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends organizational security assessment data to an external API, which may include sensitive incident response context, system inventories, compliance requirements, or contact information.

Mitigation: Review the provider's security, retention, deletion, data residency, and access-control practices before use, and avoid submitting real incident evidence, credentials, tokens, private keys, regulated personal data, emergency contact lists, or detailed internal system inventories unless those controls have been approved.

Risk: Generated playbooks may include operational, escalation, or regulatory guidance that is not sufficient for a specific organization or jurisdiction.

Mitigation: Have security, legal, compliance, and incident-response stakeholders review generated playbooks before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-ir-playbook-generator)
- [API documentation](https://api.mkkpro.com:8118/docs)
- [API gateway route](https://api.mkkpro.com/security/ir-playbook-generator)
- [OpenAPI specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON response containing playbook sections suitable for documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response includes executive summary text, response phases, roles, communication templates, escalation procedures, legal considerations, contact lists, session ID, and timestamp.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
