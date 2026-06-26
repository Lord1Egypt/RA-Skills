## Description: <br>
Travel Search helps agents compare flights, hotels, Airbnb stays, car rentals, ferries, and destination essentials across multiple travel providers, then present concise recommendations with prices and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adrianetti](https://clawhub.ai/user/adrianetti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to search and compare travel options, optimize trip routes and itineraries, and produce actionable travel recommendations with live provider data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel searches send trip details to named travel providers. <br>
Mitigation: Install only if comfortable sharing travel search details with those providers, and avoid including unnecessary personal information. <br>
Risk: Booking links and prices can change before purchase. <br>
Mitigation: Verify booking links and prices directly with the provider before paying. <br>
Risk: Hidden-city fares can create airline-policy and baggage issues. <br>
Mitigation: Review hidden-city fare restrictions carefully before booking. <br>
Risk: Optional Airbnb and Google Flights components are separate packages. <br>
Mitigation: Install optional components only after confirming that those packages are trusted for the deployment environment. <br>


## Reference(s): <br>
- [Travel Search on ClawHub](https://clawhub.ai/adrianetti/travel-search) <br>
- [README](README.md) <br>
- [Roadmap](ROADMAP.md) <br>
- [Kiwi.com Flight Search](references/flights.md) <br>
- [Skiplagged Flights, Hotels, and Car Rentals](references/skiplagged.md) <br>
- [Trivago Hotel and Accommodation Search](references/hotels.md) <br>
- [Ferryhopper Ferry Search](references/ferries.md) <br>
- [Airbnb Short-Stay and Apartment Search](references/airbnb.md) <br>
- [Google Flights via fli](references/google-flights.md) <br>
- [Smart Price Deal Selection](references/price-tools.md) <br>
- [Trip Planner](references/trip-planner.md) <br>
- [Multi-City Optimizer](references/multi-city.md) <br>
- [Travel Intel Destination Intelligence](references/travel-intel.md) <br>
- [MCP Protocol](https://modelcontextprotocol.io/) <br>
- [Airbnb MCP Server](https://github.com/borski/mcp-server-airbnb) <br>
- [fli Google Flights Tool](https://github.com/punitarani/fli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendations with inline commands, provider links, and structured travel options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live prices, route details, dates, provider trade-offs, direct booking links, and travel-intelligence notes.] <br>

## Skill Version(s): <br>
1.5.0 (source: server evidence release.version; roadmap marks v1.5.0 Travel Intel complete) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
