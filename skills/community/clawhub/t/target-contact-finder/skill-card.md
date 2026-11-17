## Description:

Finds target travel and B2B customer contacts from structured search criteria and helps import confirmed records into a CRM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tourmind](https://clawhub.ai/user/tourmind)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, business development, and CRM operators use this skill to translate natural-language target-customer requests into structured lead searches, review matching travel and B2B contacts, and import confirmed contacts into a CRM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and CRM lead or contact data are sent to a raw IP address over unencrypted HTTP.

Mitigation: Use the skill only after trusting the service operator, and prefer an HTTPS endpoint before sending sensitive or regulated CRM data.

Risk: Broad activation language can cause the skill to engage for many lead-search or customer-search requests.

Mitigation: Review and narrow the trigger scope before deployment in shared or high-volume environments.

Risk: Batch CRM import can create business records containing personal contact data.

Mitigation: Require explicit user confirmation before import and verify privacy, consent, and compliance responsibilities for the target market.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tourmind/skills/target-contact-finder)
- [Publisher profile](https://clawhub.ai/user/tourmind)
- [Customer profile search API endpoint](http://39.108.114.224:9059/skill/search_customer_profile)
- [Batch customer import API endpoint](http://39.108.114.224:9059/skill/batch_import_customer)

## Skill Output:

**Output Type(s):** [text, API calls, JSON, guidance]

**Output Format:** [Markdown text with JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user_key before API calls; search results should be shown for user confirmation before CRM import.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
