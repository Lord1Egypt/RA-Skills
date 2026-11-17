## Description:

Queries JisuAPI with a 17-character VIN to identify vehicle make, model year, displacement, fuel details, and related oil or gearbox information by vehicle model ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up vehicle details from a 17-character VIN and optionally retrieve oil or gearbox details for a returned car model ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: VINs, car model IDs, and the JISU_API_KEY are sent to JisuAPI for lookup.

Mitigation: Use the skill only when that provider call pattern is acceptable; restrict and rotate the API key and avoid confidential vehicle records unless privacy requirements allow it.

Risk: Results depend on live JisuAPI availability, account permissions, and request quota.

Mitigation: Check returned http_error or api_error messages and verify key status, entitlement, and rate limits before relying on the result.

## Reference(s):

- [JisuAPI VIN Vehicle Identification Number API](https://www.jisuapi.com/api/vin/)
- [JisuAPI](https://www.jisuapi.com/)
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/vin)
- [ClawHub publisher profile](https://clawhub.ai/user/jisuapi)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses from VIN, oil, and gearbox lookups, with agent-facing guidance for command usage and summarization.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends VINs or car model IDs to JisuAPI over HTTPS.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
