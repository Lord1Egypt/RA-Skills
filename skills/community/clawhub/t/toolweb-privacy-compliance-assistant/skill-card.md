## Description:

Generates Privacy Impact Assessment and Data Protection Officer advisory reports from organization, personal-data, processing-purpose, system, and third-party sharing details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Privacy, legal, and compliance teams use this skill to draft PIA, ROPA, legal basis, data subject rights, third-party risk, retention, transfer, and remediation guidance from a structured privacy inventory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends privacy inventory metadata, system names, vendor relationships, and processing purposes to an external ToolWeb.in API.

Mitigation: Use only authorized, necessary compliance inventory details and avoid raw personal records, secrets, credentials, customer lists, or unnecessary sensitive data unless appropriate data-handling assurances are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-privacy-compliance-assistant)
- [ToolWeb Privacy Assistant API](https://portal.toolweb.in/apis/compliance/privacy-assistant)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or JSON compliance report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes PIA, ROPA, legal basis analysis, data subject rights checklist, third-party risk summary, retention and deletion guidance, cross-border transfer analysis, and prioritized remediation actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
