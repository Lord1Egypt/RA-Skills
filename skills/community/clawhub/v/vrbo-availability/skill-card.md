## Description:

Check day-by-day Vrbo availability (the booking calendar) for a known listing over a date window. Use when a user asks whether a listing on Vrbo is open on specific dates. Powered by StayingAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel automation agents use this skill to check whether a known Vrbo listing is available for specific dates or date ranges. It helps agents request availability data from StayingAPI and interpret day-by-day calendar results, async jobs, empty results, and platform limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a StayingAPI key, and the evidence security summary flags persistent live API key storage without clear secret-storage safeguards.

Mitigation: Use a sandbox key for evaluation, avoid storing live keys in general shell profiles, and store production keys in a protected secret manager or narrowly scoped runtime secret configuration that can be revoked or rotated.

Risk: Live availability requests can involve async polling and rate limits, which may fail or return empty results.

Mitigation: Honor Retry-After, use bounded backoff between polling attempts, and treat failed or empty job results as explicit outcomes rather than assuming availability.

## Reference(s):

- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [Authentication setup](references/auth-setup.md)
- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/vrbo-availability)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with REST request details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or explain JSON API responses from StayingAPI availability and job polling endpoints.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
