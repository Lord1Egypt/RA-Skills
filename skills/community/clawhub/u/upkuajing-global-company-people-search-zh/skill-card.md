## Description:

Searches Upkuajing global company and people data to help agents find overseas companies, decision makers, contact channels, company details, and B2B trade leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade, procurement, sales, and agency users use this skill to search for global companies and people, retrieve company or person details, and collect contact information for B2B lead development. Agents can use it to choose the right Upkuajing API script, prepare search parameters, and return structured results or saved result files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and retrieved contact records are sent to and processed by Upkuajing.

Mitigation: Disclose third-party processing before use and only submit queries and use contact data where privacy, consent, and anti-spam rules allow it.

Risk: The skill handles an API key and may save it under ~/.upkuajing/.env.

Mitigation: Prefer environment-variable injection when possible, restrict permissions on ~/.upkuajing, and never print or share the .env file.

Risk: Company and people search results can include personal contact data and may be retained in local task result files.

Mitigation: Limit searches to necessary records, protect task_data outputs, and delete retained result files when they are no longer needed.

Risk: API calls may incur charges, especially larger list searches and batch detail or contact lookups.

Mitigation: Check current pricing, explain expected call or ID counts, and wait for explicit user confirmation before paid operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/upkuajing-global-company-people-search-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Company list API reference](references/company-list-api.md)
- [Human list API reference](references/human-list-api.md)
- [Company detail API reference](references/company-detail-api.md)
- [Human detail API reference](references/human-detail-api.md)
- [Contact API reference](references/contact-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands, JSON API responses, and JSONL result files for list searches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY. Paid searches can create task result files and should be confirmed before execution.]

## Skill Version(s):

1.0.10 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
