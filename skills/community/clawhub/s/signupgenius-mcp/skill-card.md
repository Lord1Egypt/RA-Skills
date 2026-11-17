## Description:

Read sign-up sheets, slot reports, and groups on SignUpGenius, and add members to your groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to their own SignUpGenius account for reading profile, group, sign-up, RSVP, and slot-report information, with limited write actions for adding group members and RSVPing to public sign-up slots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party MCP package that can access a SignUpGenius account session.

Mitigation: Pin and review the package version before installation, and install only when the publisher and package are trusted.

Risk: Reusable account credentials or session tokens may be exposed through local configuration or browser-extension access.

Mitigation: Avoid storing secrets in project-level config files, restrict config file permissions, and rotate credentials if exposure is suspected.

Risk: The skill includes write tools for adding group members and RSVPing to public sign-up slots.

Mitigation: Require manual confirmation before invoking write tools and review the target group, person, public sign-up, and slot before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/signupgenius-mcp)
- [signupgenius-mcp npm package](https://www.npmjs.com/package/signupgenius-mcp)
- [SignUpGenius](https://www.signupgenius.com)
- [fetchproxy extension](https://github.com/chrischall/fetchproxy)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agent use of an MCP server with SignUpGenius account authentication and limited write tools.]

## Skill Version(s):

1.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
