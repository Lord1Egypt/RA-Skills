## Description: <br>
schedule-planner-cxf helps an agent plan business or leisure trips, compare transport and hotel options, and prepare itinerary summaries or HTML trip pages using AMap and Tuniu workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptocxf](https://clawhub.ai/user/cryptocxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, assistants, and developers use this skill to compare routes, dates, and hotels; plan multi-city itineraries; and prepare booking or payment guidance. Users should review all passenger, itinerary, price, destination, and order details before any booking or payment step. <br>

### Deployment Geography for Use: <br>
Global, subject to AMap and Tuniu service coverage. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use travel API keys and passenger identity data. <br>
Mitigation: Keep credentials and passenger details local, avoid storing default identity data unless necessary, and remove generated trip files when the trip is complete. <br>
Risk: The skill can create real unpaid travel orders and payment pages. <br>
Mitigation: Review every passenger, itinerary, price, destination URL, and order action before confirming an order or completing payment. <br>
Risk: Generated JSON or HTML trip files may include itinerary, order, or payment-link details. <br>
Mitigation: Share generated files only with intended recipients and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cryptocxf/schedule-planner-cxf) <br>
- [AMap API documentation](https://lbs.amap.com/) <br>
- [Transport comparison reference](references/transport-comparison.md) <br>
- [City guides reference](references/city-guides.md) <br>
- [Mock mode guide](examples/mock-mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, html files, guidance] <br>
**Output Format:** [Markdown responses with tables, shell commands, JSON trip data, and generated HTML itinerary pages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local JSON and HTML files with payment-link or QR-code views; mock mode can run without external API keys.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
