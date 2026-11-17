## Description:

通用商旅出行规划助手 helps business travelers plan transportation, hotels, budgets, destination details, and HTML travel reports using travel, map, and web-search services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Business travelers and assistants use this skill to compare transport and lodging options, estimate trip budgets, assemble destination context, and produce a shareable HTML itinerary report. It is intended for normal trip-planning workflows that may call external travel, map, and search services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run external MCP packages without pinned package versions.

Mitigation: Use only in a sandboxed agent environment, pin and verify MCP package versions before enabling them, and review package behavior before use.

Risk: Trip details may include confidential meetings, business locations, traveler identity, and schedule information sent to third-party travel, map, and search services.

Mitigation: Provide only the trip details needed for planning and avoid entering confidential business information unless sharing it with those external services is acceptable.

Risk: Generated reports can embed booking links, prices, availability, and itinerary recommendations that may become stale or inaccurate.

Mitigation: Review the generated report before sharing or booking, and confirm prices, availability, and travel constraints directly with the relevant provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/skills/universal-travel-planner)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, files]

**Output Format:** [Markdown guidance with optional HTML report output and JSON MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require AMAP_WEB_KEY, AMAP_JSAPI_KEY, and AMAP_SECURITY_CODE for map-related functionality.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
