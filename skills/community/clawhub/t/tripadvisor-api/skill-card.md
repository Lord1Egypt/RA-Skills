## Description:

Query TripAdvisor location data through the Terra REST API, with an optional browser-based fallback for location details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to search TripAdvisor locations and retrieve details, photos, and reviews from a shell or script, with a browser fallback for core location details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key exposure or unexpected API usage charges.

Mitigation: Provide the key through the environment without printing it, and account for plan limits and usage charges.

Risk: The optional browser fallback uses a paired extension with fetch access.

Mitigation: Approve only tripadvisor.com with fetch capability and revoke pairing when finished.

Risk: The exact CLI and extension release binaries were outside the artifact review.

Mitigation: Verify dependency release files before installing them.

## Reference(s):

- [Terra API endpoint examples](references/terra-endpoints.md)
- [Browser fallback guide](references/web-fallback.md)
- [TripAdvisor Developers](https://www.tripadvisor.com/developers)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [TripAdvisor location data from the API or browser fallback, typically JSON, with shell command examples and usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on a valid Terra API key for API queries; the browser fallback returns core location details but not individual review text.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
