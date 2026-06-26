## Description: <br>
Recommend travel destinations based on vibe, budget, duration, and group size. Handles "suggest a trip", "where should I go", "weekend getaway", "compare X vs Y", and "plan from my saved places". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swayamg20](https://clawhub.ai/user/swayamg20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travelers and trip-planning agents use this skill to suggest or compare up to three destinations based on vibe, budget, duration, group size, saved places, and departure city. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel preferences, saved destinations, and departure details may be used in memory checks or web searches. <br>
Mitigation: Share only necessary trip details and confirm before using saved places or sensitive preferences. <br>
Risk: If the departure city is not specified, the skill defaults to Delhi, which can make travel time and cost estimates inaccurate. <br>
Mitigation: Ask for or confirm the departure city before relying on recommendations. <br>
Risk: Weather, route, and cost details are time-sensitive and may change before travel. <br>
Mitigation: Verify current weather, transit options, and prices before booking or departure. <br>


## Reference(s): <br>
- [Trip Discover on ClawHub](https://clawhub.ai/swayamg20/trip-discover) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown travel recommendations, destination comparisons, and concise trip-planning guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits recommendations to at most three destinations and includes travel time, rough per-person cost, current weather, and a tailored rationale.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
