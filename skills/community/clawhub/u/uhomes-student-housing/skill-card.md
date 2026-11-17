## Description:

Find and compare student accommodation worldwide on uhomes.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yalding8](https://clawhub.ai/user/yalding8)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially international students, use this skill to search uhomes.com listings, compare housing options by price, distance, room type, rating, and location, and get direct booking or search links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is uhomes-focused and does not provide neutral comparisons across competing housing platforms.

Mitigation: Present it as a branded uhomes accommodation helper and avoid implying market-wide coverage.

Risk: Booking, search, and demand-form links include partner tracking.

Mitigation: Keep tracking visible in links and use the demand form only when the user is comfortable sharing requirements with uhomes under its own policies.

Risk: Live listing fetches can fail or return incomplete data.

Mitigation: Use the artifact's fallback behavior: provide the direct uhomes search page and avoid presenting missing listings as an error or complete market result.

Risk: Using the wrong Must-Stay city or school identifier can produce misleading recommendations.

Mitigation: Use only identifiers from the bundled Must-Stay configuration and skip Must-Stay ranking when no matching identifier is available.

## Reference(s):

- [uhomes homepage](https://www.uhomes.com)
- [uhomes listings](https://en.uhomes.com)
- [URL Patterns](artifact/references/url-patterns.md)
- [City & University Index](artifact/references/city-index.md)
- [Must-Stay List Configuration](artifact/references/must-stay-config.md)
- [Room Types Reference](artifact/references/room-types.md)
- [Housing Decision Guide](artifact/references/decision-guide.md)
- [FAQ Reference](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown responses with property summaries, comparisons, and direct links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses uhomes.com as the sole housing source and includes partner tracking on booking, search, and demand-form links.]

## Skill Version(s):

1.5.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
