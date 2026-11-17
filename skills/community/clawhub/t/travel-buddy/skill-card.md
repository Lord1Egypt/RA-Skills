## Description:

Helps travelers compare destinations, plan and revise trips, and save day-by-day itineraries from their preferences and constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dong845](https://clawhub.ai/user/dong845)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning assistants use this skill to compare destinations, collect trip requirements, develop booking-ready itineraries, and revise plans when circumstances change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opt-in traveler profiles and trip files may contain sensitive personal preferences on the local machine.

Mitigation: Only save profiles with consent; do not enter passport numbers, payment details, passwords, or exact home addresses, and check the specific profile path before manual deletion.

Risk: Trip planning opens local intake forms and makes travel-related web requests.

Mitigation: Use it only when comfortable with local form storage and travel queries; recheck volatile prices, availability, and entry requirements before relying on a plan.

Risk: Explicitly selecting a named assistant can start a separate planning process.

Mitigation: Use --assistant codex or --assistant claude only when you intend to launch a separate planner.

## Reference(s):

- [Travel Buddy on ClawHub](https://clawhub.ai/dong845/skills/travel-buddy)
- [Destination decision and research](references/decision-and-research.md)
- [Booking-ready HTML output and safe research](references/booking-html-output.md)
- [Reusable traveler profile and local storage](references/profile-and-storage.md)
- [Trip verification](references/verification.md)

## Skill Output:

**Output Type(s):** [Travel guidance, Markdown, JSON files, HTML itineraries, Calendar files]

**Output Format:** [Conversational guidance and local JSON, HTML, and ICS files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trip assumptions, source checks, and booking options; does not itself complete purchases.]

## Skill Version(s):

2.9.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
