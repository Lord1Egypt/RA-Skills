## Description:

Uses Skiplagged's public MCP server to search flights, hotels, rental cars, flexible date calendars, and destination options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzs](https://clawhub.ai/user/wzs)

### License/Terms of Use:


## Use Case:

Travel planners, assistants, and developers use this skill to query Skiplagged MCP results for flight comparisons, flexible date checks, destination discovery, hotel searches, and car searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an unpinned Node-based mcporter executable.

Mitigation: Use a reviewed and pinned mcporter version where possible, or install and run it in a sandboxed environment.

Risk: Travel search details are sent to Skiplagged's public MCP service.

Mitigation: Invoke the skill only for searches that need Skiplagged results and avoid adding unnecessary sensitive personal details.

Risk: The skill may trigger broadly for general travel planning requests.

Mitigation: Use it when Skiplagged flight, hotel, car, destination, or fare-calendar results are specifically useful.

Risk: Prices, availability, and hidden-city itineraries can change or carry traveler constraints.

Mitigation: Present results as point-in-time, include booking or deep links when available, and clearly caveat hidden-city checked-bag and missed-leg implications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzs/skills/skiplagged-flights)
- [Skiplagged](https://skiplagged.com)
- [Skiplagged MCP docs and privacy notes](https://skiplagged.github.io/mcp/)
- [MCPorter CLI README](https://raw.githubusercontent.com/steipete/mcporter/main/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown bullets or labeled lines, optionally grounded in JSON MCP results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mobile-friendly summaries; no markdown tables; includes booking or deep links when returned.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
