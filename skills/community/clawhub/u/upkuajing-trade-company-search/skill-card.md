## Description:

Find companies, global buyers, trade orders, company details, and contact information using UpKuaJing customs trade data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warmc](https://clawhub.ai/user/warmc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for import/export market research, lead generation, buyer and supplier discovery, and customs trade record analysis through the UpKuaJing API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid remote API service and can incur charges for searches, detail lookups, and contact lookups.

Mitigation: Confirm expected query volume and fee impact before running billable API calls, and use the pricing endpoint or UpKuaJing price page for current pricing.

Risk: The skill may store an API key in a plaintext home-directory file.

Mitigation: Prefer environment-based secret handling where possible, restrict file permissions on ~/.upkuajing/.env, and rotate the key if it is exposed in logs or transcripts.

Risk: Search result data can be persisted locally as task metadata and JSONL result files.

Mitigation: Review local result files for sensitive business or contact data and remove them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/warmc/skills/upkuajing-trade-company-search)
- [Publisher profile](https://clawhub.ai/user/warmc)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Company Detail API reference](references/company-detail-api.md)
- [Company List API reference](references/company-list-api.md)
- [Contact Fetch API reference](references/contact-fetch-api.md)
- [Trade List API reference](references/trade-list-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or JSONL API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search scripts may persist task metadata and result files locally under artifact/task_data; API key setup uses UPKUAJING_API_KEY.]

## Skill Version(s):

1.0.6 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
