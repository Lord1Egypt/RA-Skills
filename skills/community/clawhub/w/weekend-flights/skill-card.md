## Description:

Search flights for quick weekend getaways by helping an agent run flyai CLI flight searches for Friday/Saturday departures and Sunday/Monday returns, with related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search weekend flight options, compare routes and prices from flyai CLI output, and present booking links for short getaway planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to install and run an unpinned global npm CLI package before answering travel queries.

Mitigation: Install a reviewed, pinned version of @fly-ai/flyai-cli manually in an isolated environment before enabling the skill.

Risk: Booking links and travel results are third-party commercial outputs rather than neutral advice.

Mitigation: Treat returned booking links as commercial links and verify pricing, itinerary details, and terms with the provider before purchase.

## Reference(s):

- [Weekend Flights ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/weekend-flights)
- [dingtom336-gif ClawHub publisher profile](https://clawhub.ai/user/dingtom336-gif)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when setup or execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to be derived from flyai CLI output and include booking links when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
