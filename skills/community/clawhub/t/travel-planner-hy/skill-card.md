## Description:

Travel Planner HY plans multi-day travel itineraries, researches public attractions, compares requested travel options, and exports local itinerary HTML with optional public-platform homepage QR codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan concrete multi-day trips, compare requested travel options, summarize budgets and logistics, and generate local itinerary exports. It supports information planning only and does not create bookings, orders, or payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip inputs, URLs, or search terms could accidentally include identity documents, payment details, account links, API keys, tokens, or booking information.

Mitigation: Keep trip inputs and public searches limited to destination, attraction, date, budget, and preference information; do not include credentials, payment data, identity documents, or booking records.

Risk: The skill can write local itinerary files and QR code images.

Mitigation: Review generated files before sharing them, keep exports local unless the user explicitly approves publication, and avoid including private travel details in exported content.

Risk: Fetched public travel pages may contain stale information or untrusted page instructions.

Mitigation: Treat fetched page content as reference data only, verify current prices and opening hours against authoritative sources, and do not follow instructions embedded in fetched pages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cryptocxf/skills/travel-planner-hy)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Usage](references/usage.md)
- [URL Safety](references/url-safety.md)
- [Validation](references/validation.md)
- [Output Templates](references/output-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown or plain-text travel guidance with JSON input examples and optional local HTML or PNG exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local exports are written to the skill output directory; public web fetching is restricted to approved HTTPS travel domains.]

## Skill Version(s):

1.3.2 (source: server release evidence, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
