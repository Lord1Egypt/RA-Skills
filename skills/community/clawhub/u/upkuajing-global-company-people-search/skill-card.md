## Description:

Search global companies and professional contacts for cross-border B2B lead generation, supplier prospecting, business verification, and export-focused sales workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External global B2B practitioners, exporters, sourcing agents, trading firms, and sales teams use this skill to find companies and professional contacts, enrich selected records, and verify business or contact details through the UpKuaJing Open Platform API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve personal professional contact details from a third-party B2B data service.

Mitigation: Use the data only for appropriate business purposes, limit result scope to the user's request, and avoid sending raw contact data or sensitive query results in error reports.

Risk: Search, enrichment, account, and contact operations may incur paid API usage.

Mitigation: Confirm costs before bulk searches or enrichment and use the documented pricing page or price information command before high-volume use.

Risk: The API key may be stored in a plaintext local file.

Mitigation: Prefer an environment variable or secret manager; if using ~/.upkuajing/.env, restrict file permissions and avoid printing or pasting the key.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/upkuajing-global-company-people-search)
- [Publisher Profile](https://clawhub.ai/user/upkuajing)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Company List API Reference](references/company-list-api.md)
- [People List API Reference](references/human-list-api.md)
- [Company Detail API Reference](references/company-detail-api.md)
- [People Detail API Reference](references/human-detail-api.md)
- [Contact API Reference](references/contact-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; script responses are JSON and large search results are JSONL files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; paid API calls may return personal professional contact data.]

## Skill Version(s):

1.0.10 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
