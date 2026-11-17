## Description:

Skill for SEO promotion by purchasing guest posts on trusted donor websites using the Serpzilla platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanislav-reshetnev](https://clawhub.ai/user/stanislav-reshetnev)

### License/Terms of Use:

MIT-0

## Use Case:

SEO specialists and webmasters use this skill with OpenClaw to search Serpzilla donor sites, prepare content, purchase guest posts or link insertions, and manage placement lifecycle actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles real Serpzilla API credentials.

Mitigation: Use a dedicated, revocable Serpzilla token with the least authority and budget possible, and avoid storing tokens in shell history or plaintext configuration.

Risk: Purchase and placement actions can spend funds, release funds, cancel orders, or remove approved backlinks.

Mitigation: Independently confirm every purchase or placement action in the Serpzilla UI before execution.

Risk: The setup relies on third-party tooling and a Docker image that are not pinned by digest in the artifact.

Mitigation: Pin and verify mcporter and the Serpzilla MCP Docker image digest before deployment.

## Reference(s):

- [Serpzilla API Documentation](https://serpzilla.com/api/)
- [SEO Actions for Managing Placements](references/placement_actions.md)
- [Serpzilla MCP Server Docker Image](https://hub.docker.com/r/stanislavusbest/serpzilla-mcp-stdio-server/tags)
- [ClawHub Skill Release](https://clawhub.ai/stanislav-reshetnev/skills/serpzilla-seo-guest-posting)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter, Docker, SERPZILLA_LOGIN, and SERPZILLA_API_TOKEN.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
