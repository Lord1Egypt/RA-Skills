## Description:

Trip Planner helps an agent gather travel requirements, research live travel facts, and produce a polished standalone HTML itinerary with maps, timelines, budgets, checklists, and source-labeled uncertainty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric6286](https://clawhub.ai/user/eric6286)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to turn destination, date, budget, party, and constraint inputs into a checked day-by-day itinerary page that can be shared and used during a trip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to read travel prices, reviews, and social-platform content through a browser, including logged-in sessions.

Mitigation: Use a separate browser profile or logged-out mode when account-linked data should not be involved, and limit the agent to reading visible travel content.

Risk: Booking, payment, passwords, and CAPTCHA handling could expose credentials or trigger unintended transactions if delegated to the agent.

Mitigation: Keep all booking and payment actions manual; the agent should not enter passwords, solve CAPTCHAs, reserve inventory, or submit orders.

Risk: Generated itinerary facts such as prices, opening hours, transport times, and reviews can be incomplete or stale.

Mitigation: Require source labels or explicit uncertainty markers in the output and re-check critical travel details with official providers before booking or departure.

Risk: Generated HTML pages load Leaflet JavaScript from a CDN and map tiles from OpenStreetMap.

Mitigation: Review generated HTML before sharing or opening in sensitive environments, and only use the remote map resources when acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eric6286/skills/trip-planner)
- [Trip Planner README](README.md)
- [Trip Planner HTML Output Spec](references/design-system.md)
- [Research Playbook & Itinerary Logic](references/research-playbook.md)
- [Efficient Web Scraping Method](references/scraping-method.md)
- [Benchmark Results](evals/benchmark.md)
- [Evaluation Prompts](evals/evals.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Standalone HTML file with embedded CSS, JavaScript, itinerary data, and Leaflet/OpenStreetMap map wiring.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one destination-specific itinerary HTML file; Leaflet CDN and OpenStreetMap tiles are the expected remote map dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
