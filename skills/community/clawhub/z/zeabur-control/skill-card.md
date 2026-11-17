## Description:

Manage KobePlay and HillStreet Zeabur projects through the authenticated Zeabur MCP connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Zeabur projects, services, deployments, domains, ports, environment settings, and logs through an authenticated connection. It guides resource verification, secret protection, rollback preparation, and post-change health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because two references in the skill could not be resolved.

Mitigation: Confirm that the named dashboard and API are the intended services for your setup before installing or using the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hillstreet-ph/skills/zeabur-control)
- [Open-Connect MCP gateway](https://open-connect.site/mcp)
- [Open-Connect API](https://open-connect.site/api/v1)
- [Open-Connect OAuth issuer](https://open-connect.site)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Guidance, Text]

**Output Format:** [Authenticated MCP operations and concise text or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports PRODUCTION_VERIFIED only after functional endpoint checks and does not include secret values.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
