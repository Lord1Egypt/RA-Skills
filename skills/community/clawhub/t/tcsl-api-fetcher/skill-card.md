## Description:

Helps agents reference the Tian Cai Shang Long (TCSL) Open Platform API catalog, module groupings, and solution mappings for restaurant, supply chain, order, payment, and member-management integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to look up TCSL Open Platform endpoints, request and response fields, base URLs, and solution-to-API mappings before drafting integration guidance or code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The solution mapping can route requests toward create, update, delete, staff, role, account, warehouse, payment, and member operations.

Mitigation: Require explicit confirmation before using or recommending those operations, and review the selected endpoint and payload manually.

Risk: Some documented test URLs use plaintext HTTP and the API areas may involve credentials, employee PII, member data, or payment account data.

Mitigation: Prefer HTTPS endpoints and do not send real credentials, employee PII, member data, or payment account data through plaintext test URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woai36d/skills/tcsl-api-fetcher)
- [TCSL platform usage documentation](https://open.tcsl.com.cn/document/1?id=1671367443003474005)
- [TCSL API call conventions](https://open.tcsl.com.cn/document/1?id=1671382857745956883)
- [API inventory](references/_all_apis.json)
- [Organized API modules](references/_modules_organized.json)
- [Solution API mapping](solutions/_solution_api_mapping.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with API names, endpoint details, parameters, and implementation snippets when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only reference output; endpoint execution should remain user-confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
