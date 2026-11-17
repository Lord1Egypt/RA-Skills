## Description:

RollingGo Hotel Search helps agents search hotels, apply travel filters, inspect hotel details and room pricing, and surface booking or detail links through the RollingGo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnchenkai](https://clawhub.ai/user/cnchenkai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search hotels by destination, dates, occupancy, budget, star rating, tags, brand, or distance, then compare current pricing and room details. It is scoped to hotel discovery, pricing, and booking-link handoff rather than flights, trains, transfers, or car rentals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation includes a shared public API key and supports passing API keys on command lines or in Markdown configuration.

Mitigation: Prefer a user-owned API key, load it from an environment variable, and avoid putting secrets in command arguments or Markdown files.

Risk: The security evidence flags always-latest third-party package execution and global upgrade guidance.

Mitigation: Pin RollingGo to a reviewed version and run it in an isolated environment before using it with real travel-search details.

Risk: Hotel searches and filters are sent through a third-party hotel CLI/API.

Mitigation: Avoid unnecessary personal or sensitive travel details and review the third-party service terms before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnchenkai/skills/rollinggo-searchhotel-skill)
- [Publisher profile](https://clawhub.ai/user/cnchenkai)
- [RollingGo homepage](https://mcp.agentichotel.cn)
- [RollingGo API key application](https://mcp.agentichotel.cn/apply)
- [RollingGo API Key Configuration](references/env.md)
- [RollingGo NPX Reference](references/rollinggo-npx.md)
- [RollingGo UV Reference](references/rollinggo-uv.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON-oriented CLI output handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIGOHOTEL_API_KEY; CLI results are JSON by default and may include booking URLs and hotel detail links.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
