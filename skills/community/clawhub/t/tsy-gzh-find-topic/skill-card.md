## Description:

Calls a backend API to retrieve popular WeChat public account topic recommendations and returns the raw data field.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangshiyegit](https://clawhub.ai/user/tangshiyegit)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to request trending topic suggestions for WeChat public accounts through a configured backend service. It returns the service response data directly without analysis or rewriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an API key in the request URL to a configurable backend, which may expose credentials through logs or untrusted endpoints.

Mitigation: Use an HTTPS allowlisted BASE_URL, trust the configured backend before installation, rotate keys that may have appeared in logs, and prefer moving credentials to an authorization header.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, Text]

**Output Format:** [Raw API response data as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TSY_API_KEY in .env and uses TSY_API_URL when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
