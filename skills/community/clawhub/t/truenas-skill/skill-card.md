## Description:

Manage TrueNAS SCALE via API, including pool health, datasets, snapshots, alerts, services, apps, Dockge container stacks, bookmarks, and related homelab services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anotb](https://clawhub.ai/user/anotb)

### License/Terms of Use:

MIT

## Use Case:

External developers, homelab operators, and storage administrators use this skill to inspect and manage TrueNAS SCALE systems and adjacent self-hosted services through agent-produced commands, API calls, and configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad, high-impact control over a NAS and related homelab services.

Mitigation: Use least-privilege API keys and review every mutating command before execution.

Risk: TLS certificate validation may be relaxed for self-signed TrueNAS connections and Dockge credentials may be handled as environment variables.

Mitigation: Prefer HTTPS with certificate validation enabled through TRUENAS_VERIFY_TLS=1 and avoid plaintext Dockge credentials where possible.

Risk: Bulk Dockge stack updates and recursive ACL examples can affect multiple services or datasets at once.

Mitigation: Scope updates to named stacks and adapt recursive ACL examples to the target environment before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anotb/skills/truenas-skill)
- [TrueNAS App Installation Guide](references/app-installation.md)
- [Media Management](references/media-management.md)
- [Download Clients](references/downloads.md)
- [Homelab Services](references/homelab-services.md)
- [Books & Media](references/books-and-media.md)
- [Bookmarks - Karakeep](references/bookmarks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples that require user-provided TrueNAS, Dockge, or homelab service credentials.]

## Skill Version(s):

1.2.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
