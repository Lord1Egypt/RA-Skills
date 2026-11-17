## Description:

Generates customized, phased data breach incident response playbooks with tool recommendations and compliance checklists based on an organization's profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, incident responders, and compliance officers use this skill to generate tailored breach response plans from organization profile, data type, security tooling, and compliance inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive breach-response context to a third-party API without sufficient privacy, retention, or handling disclosure in the provided evidence.

Mitigation: Review provider and API terms before use, and avoid sending real breach details, exact tool inventories, regulated-data specifics, company names, user IDs, or session identifiers unless approved by the organization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-data-breach-response)
- [Data Breach Response API Route](https://api.mkkpro.com/security/data-breach-response)
- [Data Breach Response API Docs](https://api.mkkpro.com:8106/docs)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [text, json, api calls, guidance]

**Output Format:** [Markdown guidance with JSON request and response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include phased timelines, response actions, tool recommendations, and compliance checklist items.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
