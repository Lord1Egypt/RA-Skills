## Description:

Helps agents summarize public Tongcheng Travel hotel and flight pages, including prices, ratings, schedules, and light itinerary budget estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to compare publicly available Tongcheng hotel and flight listings, summarize prices and ratings, and estimate lightweight trip budgets. It is intended for public-page analysis and reminders, not booking, login-only actions, API reverse engineering, or bulk collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prices, schedules, and inventory may change after collection.

Mitigation: Include the collection time in summaries and treat results as advisory until checked on the live public page.

Risk: Automation could exceed the intended public-page analysis boundary.

Mitigation: Use low-frequency, user-directed summaries of public pages only; avoid booking flows, login-only actions, API reverse engineering, bulk scraping, and bypassing platform checks.

Risk: Dynamic rendering or human verification may make extracted page data incomplete.

Mitigation: Have the user open the page when needed and review extracted hotel, flight, and budget details before acting on them.

## Reference(s):

- [Tongcheng Travel](https://www.ly.com/)
- [Tongcheng Hotels](https://hotel.ly.com/)
- [Tongcheng Flights](https://flight.ly.com/)
- [ClawHub skill page](https://clawhub.ai/mike47512/skills/tongcheng)
- [ClawHub publisher profile](https://clawhub.ai/user/mike47512)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain-text summaries of public hotel, flight, itinerary, and budget information.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include collection time when summarizing prices, schedules, or inventory-sensitive information.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
