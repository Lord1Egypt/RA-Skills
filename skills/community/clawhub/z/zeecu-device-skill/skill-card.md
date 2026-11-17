## Description:

Queries Zeecu electric vehicle information, including bound vehicle lists, real-time vehicle status, and historical riding tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antgroup](https://clawhub.ai/user/antgroup)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve a user's Zeecu electric vehicle list, current status, precise location, battery and mileage details, and recent riding history from the provider API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose exact vehicle location, street addresses, VIN or frame identifiers, and recent trip patterns.

Mitigation: Run it only in a trusted workspace and share returned vehicle or trip data only with users who are authorized to see it.

Risk: The query script can save a live API key to config.json in plaintext after resolving credentials.

Mitigation: Prefer the API_KEY environment variable, avoid command-line key arguments, protect or delete config.json after use, and rotate the key if it may have been saved or synced unintentionally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antgroup/skills/zeecu-device-skill)
- [Publisher profile](https://clawhub.ai/user/antgroup)
- [API specification](artifact/references/api-spec.md)
- [Zeecu mPaaS API endpoint](https://cn-hangzhou-mgs-gw.cloud.alipay.com/mgw.htm)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses with Markdown setup and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vehicle identifiers, precise location, addresses, real-time status, battery and mileage data, trip records, or device-selection prompts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
