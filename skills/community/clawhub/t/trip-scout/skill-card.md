## Description:

Trip Scout helps individuals and families search flights and hotels, evaluate hotel risk, monitor airfare, plan road trips, generate itinerary maps, and find car-rental pickup and return locations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[treesan](https://clawhub.ai/user/treesan)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-planning agents use Trip Scout to turn trip constraints into flight and hotel recommendations, road-trip routes, map outputs, and ongoing travel preference memory. It is intended for personal and family travel planning with user-supplied accounts and API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles and stores travel-site sessions, cookies, and API tokens.

Mitigation: Use a dedicated low-privilege environment, avoid pasting high-value browser cookies, protect local session directories with owner-only permissions, and clear ~/.xiaohongshu/ and ~/.ctrip/ after use.

Risk: One workflow can log account session cookies.

Mitigation: Review generated logs before sharing them and rotate or clear affected sessions after troubleshooting.

Risk: The skill recommends mutable third-party package execution in at least one path.

Mitigation: Pin and review package versions before running commands that may receive tokens or account context.

Risk: Travel prices, availability, routes, and booking requirements can change after the agent produces recommendations.

Mitigation: Verify critical flights, hotels, rental locations, route restrictions, and reservation requirements directly with the relevant service before booking or travel.

## Reference(s):

- [Trip Scout README](README.md)
- [Flight Search Workflow](references/flight-search.md)
- [Hotel Search Workflow](references/hotel-search.md)
- [Hotel Review Analysis](references/review-analysis.md)
- [Hotel Trust System](references/hotel-trust-system.md)
- [Trip Planning Methodology](references/trip-planning.md)
- [Road Trip Planning Methodology](references/road-trip-planning.md)
- [Car Rental Store Lookup](references/car-rental-stores.md)
- [Xiaohongshu Hotel Research](references/xhs-hotel-research.md)
- [Xiaohongshu Route Search](references/xhs-route-search.md)
- [Memory Format](references/memory-format.md)
- [Dianping Research Workflow](references/dianping-research.md)
- [Trip Scout ClawHub Page](https://clawhub.ai/treesan/skills/trip-scout)
- [Amap LBS Skill](https://clawhub.ai/lbs-amap/skills/amap-lbs-skill)
- [Amap MCP Server Documentation](https://developer.amap.com/api/mcp-server/summary)
- [Spider_XHS](https://github.com/cv-cat/Spider_XHS)
- [trip-map-builder](https://github.com/hiyeshu/trip-map-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, configuration snippets, and generated itinerary artifacts such as HTML map pages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local travel memory, hotel blacklist, flight-price history, and itinerary output files when workflows are executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
