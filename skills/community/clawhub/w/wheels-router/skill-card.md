## Description:

Plan public transit trips globally using Wheels Router (Hong Kong) and Transitous (worldwide).

This skill is ready for commercial/non-commercial use.

## Publisher:

[anscg](https://clawhub.ai/user/anscg)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search locations and plan public transit trips, with detailed route, schedule, platform, and fare information for Hong Kong and broader routing coverage in major global cities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup examples use unpinned npx-executed packages that can run mutable third-party code on the user's machine.

Mitigation: Pin reviewed versions of mcporter and mcp-remote, or run the MCP bridge in a restricted environment before installation.

Risk: Transit planning may send sensitive home, work, or routine travel locations to a remote routing service.

Mitigation: Avoid entering sensitive travel locations unless the user is comfortable sharing them with the routing service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anscg/skills/wheels-router)
- [Wheels Router MCP server](https://mcp.justusewheels.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route options, transit legs, fare ranges, schedule details, platform information, and location search results.]

## Skill Version(s):

0.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
