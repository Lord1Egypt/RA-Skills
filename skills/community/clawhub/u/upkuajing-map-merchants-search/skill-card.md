## Description:

Pull bulk Google Maps business data with radius-based filters to gather merchant contact information, analyze market density, and find distributors or overseas buyers for offline business expansion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External business development, field sales, distributor, brand operations, and regional management teams use this skill to search global merchant data by geography, radius, industry, keyword, and contact availability for B2B lead generation and territory planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Merchant searches use a paid API service and may consume account balance.

Mitigation: Confirm current pricing and expected call volume before paid searches, especially for bulk queries.

Risk: The skill reads or writes an UpKuaJing API key in ~/.upkuajing/.env.

Mitigation: Restrict local permissions on the credential file and avoid sharing the key in prompts, logs, or reports.

Risk: Search results and task metadata may contain business contact data in local files.

Mitigation: Limit access to generated task_data and geography output files, and delete them when they are no longer needed.

Risk: Error reports can include request context and response details.

Mitigation: Review report content before submission and avoid including sensitive business data.

Risk: The skill performs a version-check request when API helpers run.

Mitigation: Review network access expectations before installation and operation.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/upkuajing/skills/upkuajing-map-merchants-search)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Merchants Search API](references/merchants-search-api.md)
- [Country List API](references/country-list-api.md)
- [Province List API](references/province-list-api.md)
- [City List API](references/city-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON results from the helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Merchant searches can produce local JSONL result files and task metadata; geography lookups can produce local JSON files.]

## Skill Version(s):

1.0.6 (source: server evidence release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
