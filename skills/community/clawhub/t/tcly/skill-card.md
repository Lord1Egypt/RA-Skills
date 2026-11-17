## Description:

Travel In China is a bilingual assistant for collecting inbound tourism requirements for China and submitting structured lead data to Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijingxu007](https://clawhub.ai/user/lijingxu007)

### License/Terms of Use:

MIT-0

## Use Case:

Travel service teams use this skill to collect international travelers' China trip requirements in Chinese or English, confirm the details with the user, and submit structured lead records for follow-up. It is intended for workflows that handle contact details, nationality, destination preferences, budget, dietary needs, guide language, and visa-assistance requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and stores personal travel and contact details in Feishu Bitable.

Mitigation: Use a dedicated Feishu app and table with limited permissions, obtain user consent before submission, and define retention and deletion procedures.

Risk: The packaged instructions mix inbound lead collection with itinerary CRUD behavior, which may confuse expected operation.

Mitigation: Review and resolve the conflicting instructions before broad deployment.

## Reference(s):

- [Travel In China ClawHub listing](https://clawhub.ai/lijingxu007/skills/tcly)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Conversational text with structured Feishu Bitable record submissions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app and Bitable credentials configured through environment variables.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
