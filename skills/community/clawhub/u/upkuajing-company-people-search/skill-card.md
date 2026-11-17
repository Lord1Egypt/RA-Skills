## Description:

Search UpKuaJing company and people data, including business registration, background information, and contact details such as email, phone, and WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warmc](https://clawhub.ai/user/warmc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for customer development, business background checks, and talent search by querying company and people records through the UpKuaJing Open Platform API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores or reads an UpKuaJing API key and the evidence flags unsafe, under-scoped secret handling.

Mitigation: Provide the API key through a safer secret mechanism where possible, restrict permissions on `~/.upkuajing`, and do not allow the agent to print `~/.upkuajing/.env`.

Risk: Company, people, and contact searches send user queries and identifiers to UpKuaJing and may return personal contact data.

Mitigation: Run the skill only in an approved environment and treat returned people or contact records as regulated personal data.

Risk: API calls can incur paid usage and list searches can perform multiple requests.

Mitigation: Confirm expected paid usage before execution, use current pricing from UpKuaJing, and avoid unnecessary enrichment calls.

Risk: Search results can be retained in local `task_data` JSONL files.

Mitigation: Restrict access to retained result files and delete them when they are no longer needed.

## Reference(s):

- [Company List API Reference](references/company-list-api.md)
- [People List API Reference](references/human-list-api.md)
- [Company Detail API Reference](references/company-detail-api.md)
- [People Detail API Reference](references/human-detail-api.md)
- [Contact API Reference](references/contact-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing API Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Text, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [List searches may write JSONL result files under task_data; API calls require UPKUAJING_API_KEY and can incur fees.]

## Skill Version(s):

1.0.6 (source: evidence release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
