## Description:

Uses the RollingGo CLI to search hotels, filter candidates by destination, dates, star rating, budget, tags, or distance, retrieve hotel tags, and fetch hotel details and room pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longcreat](https://clawhub.ai/user/longcreat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search hotels, compare structured hotel data and current room prices, inspect tags and room details, and surface booking links when a user has selected a hotel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to fetch or upgrade unpinned latest RollingGo CLI packages at runtime.

Mitigation: Use a pinned, reviewed RollingGo CLI version and avoid global upgrades unless the release has been reviewed.

Risk: The skill handles a RollingGo API key and documents command-line API-key arguments and broad shell environment import as options.

Mitigation: Inject only ROLLINGGO_API_KEY through a scoped skill environment, avoid command-line API-key arguments, and avoid broad shell environment import unless credential exposure is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longcreat/skills/search-hotel)
- [RollingGo official site](https://rollinggo.store)
- [RollingGo API key application](https://rollinggo.store/apply)
- [RollingGo NPX reference](references/rollinggo-npx.md)
- [RollingGo UV reference](references/rollinggo-uv.md)
- [Claw host environment reference](references/claw-host-env.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ROLLINGGO_API_KEY; RollingGo CLI command results default to JSON on stdout when executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
