## Description:

Compare real-time flight and train ticket prices across major platforms with direct booking links, train availability, and discount condition details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amurtiger01](https://clawhub.ai/user/amurtiger01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to compare flight and train options for domestic China and international routes, including live train availability, available flight prices, booking links, and fare restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel route and date details may be sent to listed travel services during searches.

Mitigation: Use the skill only for routes and dates the user is comfortable sharing with those services.

Risk: Optional API keys can be exposed if stored permanently in plaintext shell profiles or command history.

Mitigation: Prefer temporary environment variables or a secret manager, and rotate any key that may have been exposed.

Risk: The optional Amadeus SDK install adds dependency risk when installed unpinned or into a shared environment.

Mitigation: Install optional dependencies only when needed, pin versions, and use an isolated environment.

## Reference(s):

- [Ticket Price Comparison Platform Detailed Guide](references/platforms_guide.md)
- [Firecrawl](https://firecrawl.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tabular search results, direct links, discount notes, and optional setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live or recently fetched travel prices, seat availability, route-specific search tips, and booking platform links.]

## Skill Version(s):

1.2.7 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
