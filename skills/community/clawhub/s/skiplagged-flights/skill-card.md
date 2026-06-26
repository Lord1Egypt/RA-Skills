## Description: <br>
Use when the user asks to find flights, compare itineraries, search hidden-city routes, check cheapest dates, explore destinations, search hotels, plan a trip, or get general flights and trip-planning help grounded in official Skiplagged MCP results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzs](https://clawhub.ai/user/wzs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to query Skiplagged's public MCP server for flights, hotels, cars, flexible-date calendars, and destination discovery. It helps present concise travel-search results with booking links, price and routing tradeoffs, and hidden-city caveats when relevant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel-search details are sent to Skiplagged's public MCP service. <br>
Mitigation: Use the skill only for explicit flight, hotel, car, or flexible-date searches, and avoid entering unnecessary personal information. <br>
Risk: The skill depends on the mcporter CLI being installed and available on PATH. <br>
Mitigation: Install and verify mcporter before use, and inspect the MCP tool schemas with the documented list command when parameters are uncertain. <br>
Risk: Flight prices, availability, and hidden-city itinerary details can change quickly. <br>
Mitigation: Treat results as point-in-time, encourage confirmation through returned booking links or Skiplagged directly, and include checked-bag and missed-leg caveats for hidden-city itineraries. <br>


## Reference(s): <br>
- [Skiplagged](https://skiplagged.com) <br>
- [Skiplagged MCP docs and privacy notes](https://skiplagged.github.io/mcp/) <br>
- [Skiplagged public MCP server](https://mcp.skiplagged.com/mcp) <br>
- [MCPorter CLI README](https://raw.githubusercontent.com/steipete/mcporter/main/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/wzs/skiplagged-flights) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON results from MCP calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise, mobile-friendly bullets or labeled lines; top 3-5 results by default; no markdown tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
