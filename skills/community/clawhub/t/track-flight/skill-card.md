## Description:

Track flights in real time with status, gate, terminal, delay, aircraft, and live position details from AviationStack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafaforesightai](https://clawhub.ai/user/rafaforesightai)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up flight status by IATA flight number and present readable flight details for travel planning or operational awareness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the AviationStack API key and flight lookup over unencrypted HTTP.

Mitigation: Prefer an HTTPS-capable AviationStack plan or another provider, use a limited and rotatable API key, and rotate any key already used through the HTTP endpoint.

Risk: Persisting the API key in a shared shell profile can expose the credential to other users or processes on the same system.

Mitigation: Store the key only in an appropriate local environment or secret-management mechanism and avoid adding it to shared shell profile files.

## Reference(s):

- [AviationStack API Setup](references/api-setup.md)
- [AviationStack free API signup](https://aviationstack.com/signup/free)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Formatted terminal text with optional raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AVIATIONSTACK_API_KEY environment variable and the Python requests dependency.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
