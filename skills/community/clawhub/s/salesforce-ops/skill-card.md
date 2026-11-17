## Description:

Salesforce CRM integration with managed OAuth. Manage accounts, contacts, leads, opportunities, campaigns, tasks, reports, SOQL queries, and SObject records through the Salesforce REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations users use this skill to work with Salesforce CRM records, queries, reports, files, and metadata from an agent conversation. It supports read workflows and write workflows for accounts, contacts, leads, opportunities, campaigns, tasks, notes, files, SObjects, bulk jobs, custom fields, and custom objects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and allowlisting a third-party ClawLink plugin that can access and change sensitive Salesforce CRM data.

Mitigation: Review the ClawLink plugin publisher and package provenance before installing, and allow only the plugin needed for this Salesforce workflow.

Risk: Salesforce OAuth access may expose more CRM data or write capability than the user intends.

Mitigation: Connect Salesforce with the narrowest OAuth scopes practical and revoke the Salesforce OAuth connection if it is no longer needed.

Risk: Create, update, delete, clone, bulk, and custom object actions can modify or remove Salesforce records.

Mitigation: Use preview and explicit confirmation before write or destructive operations, and verify target record IDs before execution.

## Reference(s):

- [Salesforce REST API Documentation](https://developer.salesforce.com/docs/atlas.en-us.api_rest.api.meta/api_rest/)
- [Salesforce SOQL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_samples_soql.htm)
- [Salesforce SOSL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_samples_sosl.htm)
- [Salesforce SObject Reference](https://developer.salesforce.com/docs/atlas.en-us.api_rest.api.meta/api_rest/resources_sobjects.htm)
- [Salesforce Bulk API 2.0](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.api.meta/api_asynch/bulk_api_2_0.htm)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=salesforce-ops)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline bash commands and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Salesforce record data, query results, previews for write actions, connection guidance, and troubleshooting steps.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
