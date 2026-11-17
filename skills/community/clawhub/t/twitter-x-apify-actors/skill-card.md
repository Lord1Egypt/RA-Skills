## Description:

Use this skill when the user needs Twitter/X audience collection through Apify actors, including followers or following collection, optional email enrichment, username extraction from links, normalized row output, or webhook-ready payload building.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT

## Use Case:

Growth teams, founders, agencies, and operators use this skill to collect Twitter/X followers or following through Apify actors, optionally enrich usernames with emails, and return normalized rows for outreach workflows, n8n, CSV, Google Sheets, or CRM staging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized or non-compliant collection and enrichment of Twitter/X audience data can create privacy and policy risk.

Mitigation: Install and run the skill only when authorized to collect and enrich the target audience data, and keep email enrichment disabled unless there is a lawful and policy-compliant reason.

Risk: Apify API tokens can be exposed or overused if passed directly on the command line or scoped too broadly.

Mitigation: Prefer APIFY_TOKEN from a managed secret store and use a narrowly scoped, revocable Apify token.

Risk: Unpinned dependencies or install sources can change behavior in production.

Mitigation: Pin dependencies and install sources before production use.

## Reference(s):

- [Actor Contracts](references/actor-contracts.md)
- [Troubleshooting](references/troubleshooting.md)
- [Apify followers and following actor](https://console.apify.com/actors/bIYXeMcKISYGnHhBG)
- [Apify email enrichment actor](https://console.apify.com/actors/mSaHt2tt3Z7Fcwf0o)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON results with concise Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rows include targetUsername, username, sourceType, collectedAt, and optional name and email fields.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
