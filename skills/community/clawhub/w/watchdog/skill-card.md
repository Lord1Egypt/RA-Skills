## Description:

Monitors websites, APIs, ports, and scheduled tasks through Watch.dog, with tools to create checks, review status and uptime history, manage monitors and watchdogs, and configure public status pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joseshiru](https://clawhub.ai/user/joseshiru)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Watch.dog for uptime monitoring and heartbeat operations, including creating checks, viewing status, reviewing history, and managing public tracker pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Watch.dog API credentials.

Mitigation: Use a limited-scope API key when available and protect any local .env file containing WATCHDOG_API_KEY.

Risk: The remote API URL is configurable.

Mitigation: Verify that WATCHDOG_API_URL points only to the intended Watch.dog endpoint before use.

Risk: Delete and public status page operations can change account state, and confirmation is described but not enforced in code.

Mitigation: Require explicit user confirmation before delete operations and review public tracker page changes before applying them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/joseshiru/skills/watchdog)
- [ClawHub publisher profile](https://clawhub.ai/user/joseshiru)
- [Watch.dog](https://watch.dog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and setup guidance with tool-backed text results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include monitor IDs, uptime summaries, watchdog endpoint URLs, status page links, and setup instructions for WATCHDOG_API_KEY and WATCHDOG_API_URL.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
