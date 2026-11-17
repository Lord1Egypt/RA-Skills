## Description:

Provides Tencent Map Web Service API access for place search, geocoding, reverse geocoding, and nearby POI lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyleung-art](https://clawhub.ai/user/coreyleung-art)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to ask an agent to run Tencent Map lookups for locations, addresses, coordinates, and nearby points of interest through the Tencent Map Web Service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tencent Maps API keys may incur quota or billing exposure if overused or broadly scoped.

Mitigation: Use a restricted Tencent Maps API key with quotas and billing alerts before installing or running the skill.

Risk: Map queries can contain sensitive home, work, customer, or travel locations and are sent to Tencent.

Mitigation: Avoid submitting sensitive locations unless appropriate, and provide clear privacy notice to users before use.

Risk: Unencoded or weakly validated parameters can cause malformed requests or unexpected API behavior.

Mitigation: URL-encode query parameters and validate coordinates, radius, page index, and page size before execution.

Risk: The documentation advertises route planning, but the script does not implement a route action.

Mitigation: Use the implemented search, geocode, reverse_geocode, and around actions until the publisher implements or removes the advertised route feature.

## Reference(s):

- [Tencent Location Service Console](https://lbs.qq.com/dev/console/application/)
- [Tencent Map Web Service API Endpoint](https://apis.map.qq.com/ws)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON]

**Output Format:** [JSON returned by shell commands, with setup and usage guidance in Markdown documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, network access, and a TENCENT_MAP_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: evidence.release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
