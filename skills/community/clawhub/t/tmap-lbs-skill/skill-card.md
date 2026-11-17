## Description:

Tencent Maps location services for POI search, nearby search, route planning, travel planning, trajectory visualization, and map data visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vajrabodhi](https://clawhub.ai/user/vajrabodhi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Tencent Maps POIs, find nearby places, plan routes or travel itineraries, and generate map or trajectory visualization links through the tmap-lbs CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses an unpinned global CLI for map operations.

Mitigation: Use an isolated or local installation, pin the CLI package version where possible, and review the package before deployment.

Risk: The skill uses a Tencent Maps API key with location, route, and itinerary data.

Mitigation: Use a restricted API key, avoid sharing secrets in chat, and limit requests to data appropriate for Tencent Maps services.

Risk: The skill can form shell commands from user-supplied places, coordinates, and trail-data URLs.

Mitigation: Review generated commands before execution and treat shell metacharacters or untrusted trail-data URLs as unsafe input.

## Reference(s):

- [Tencent Maps Web Service API overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview)
- [Scene 1: Nearby search](references/scene1-nearby-search.md)
- [Scene 2: POI search](references/scene2-poi-search.md)
- [Scene 3: Route planning](references/scene3-route-planning.md)
- [Scene 4: Travel planning](references/scene4-travel-planner.md)
- [Scene 5: Trail map visualization](references/scene5-trail-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown responses with tmap-lbs shell commands, Tencent Maps links, and optional JSON output from CLI raw mode.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the tmap-lbs CLI for most operations and TMAP_WEBSERVICE_KEY for Tencent Maps API-backed search, route, and travel workflows.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
