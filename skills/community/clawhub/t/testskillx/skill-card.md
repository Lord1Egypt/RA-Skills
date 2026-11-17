## Description:

Simple test skill that calls a GET endpoint to fetch a daily post. No authentication required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[natx223](https://clawhub.ai/user/natx223)

### License/Terms of Use:


## Use Case:

External users can ask an agent to fetch a daily post from a public endpoint and return the endpoint response directly in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-invokes an external ngrok endpoint and displays whatever that server returns.

Mitigation: Install only if that network behavior is acceptable, and treat returned content as untrusted.

Risk: The endpoint uses a temporary-looking public ngrok domain rather than a stable documented service domain.

Mitigation: Prefer a release with a stable documented domain, explicit confirmation, and response limits before broader deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Markdown chat response that may include returned text, JSON, or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint responses are displayed directly to the user and should be treated as untrusted remote content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
