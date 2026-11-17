## Description:

Tencent Maps location service skill for POI search, nearby search, route planning, travel planning, and map or GPS track visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vajrabodhi](https://clawhub.ai/user/vajrabodhi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer location, nearby search, route planning, travel planning, and map visualization requests through Tencent Maps services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated key= URLs can expose Tencent Maps API keys in conversation history, browser history, logs, or shared links.

Mitigation: Use only restricted, temporary Tencent Maps keys and avoid workflows that return key-bearing URLs unless that exposure is acceptable.

Risk: Documented curl templates can be unsafe when populated with untrusted user-provided locations.

Mitigation: Prefer the JavaScript fetch helpers or a safe proxy, and do not run curl templates with untrusted text.

Risk: Location and route workflows may involve sensitive home, work, travel, or vehicle plate information.

Mitigation: Avoid entering sensitive home or work locations and vehicle plate numbers unless the user accepts the privacy impact.

## Reference(s):

- [Tencent Maps Web Service Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview)
- [Tencent Location Service](https://lbs.qq.com/)
- [Tencent Maps Place Search API](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch)
- [Scene 1 Keyword Search](references/scene1-keyword-search.md)
- [Scene 2 Nearby Search](references/scene2-nearby-search.md)
- [Scene 3 POI Search](references/scene3-poi-search.md)
- [Scene 4 Route Planning](references/scene4-route-planning.md)
- [Scene 5 Travel Planner](references/scene5-travel-planner.md)
- [Scene 7 Trail Map](references/scene7-trail-map.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with Tencent Maps URLs, JavaScript helper invocations, shell command examples, and JSON API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TMAP_LBS_CONFIG for Tencent Maps API-backed workflows; trail visualization links do not require an API key.]

## Skill Version(s):

1.1.32 (source: server release metadata; artifact frontmatter and package.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
