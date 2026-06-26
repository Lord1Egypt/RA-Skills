## Description: <br>
Travel Itinerary Builder creates multi-day travel itineraries with weather, points of interest, dining, transportation, budget estimates, optional booking extraction, and HTML, Markdown, or JSON outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachelchoo1212](https://clawhub.ai/user/rachelchoo1212) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to plan travel from destinations, dates, interests, budgets, and optional booking data, then produce a structured itinerary for review or printing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Gmail parsing can access email content and store travel booking details locally, including reservation numbers and itinerary data. <br>
Mitigation: Enable Gmail parsing only when needed, use narrow dates and keywords, and protect or delete generated bookings JSON after use. <br>
Risk: Optional gog and goplaces integrations can require account or API credentials. <br>
Mitigation: Review those tools before installation and grant credentials only when their access is acceptable for the trip-planning task. <br>
Risk: External weather and places data can be unavailable, stale, or incomplete. <br>
Mitigation: Review generated itineraries before travel and verify critical reservations, forecasts, venue hours, and transport details with authoritative sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rachelchoo1212/travel-itinerary-builder) <br>
- [Destination Templates](references/destination_templates.md) <br>
- [Travel Tips](references/travel_tips.md) <br>
- [wttr.in Weather Endpoint](https://wttr.in/{city}?format=j1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Travel itinerary guidance plus generated HTML, Markdown, or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional Gmail booking JSON, weather JSON, and Google Places data may be incorporated when configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
