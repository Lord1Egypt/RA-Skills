## Description: <br>
Manage TrueNAS SCALE via API, including pool health, datasets, snapshots, alerts, services, apps, Dockge container stacks, bookmarks, and related homelab services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anotb](https://clawhub.ai/user/anotb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and homelab operators use this skill to monitor and administer TrueNAS SCALE systems and adjacent self-hosted services through an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over TrueNAS and related homelab services. <br>
Mitigation: Use least-privilege API keys and require explicit manual confirmation before deletion, ACL changes, app installs or updates, workflow execution, media or download changes, game-server commands, and bulk Dockge updates. <br>
Risk: TrueNAS TLS verification is relaxed by default for self-signed certificates. <br>
Mitigation: Use HTTPS and set TRUENAS_VERIFY_TLS=1 when possible, preferably with a trusted certificate. <br>
Risk: Configured service endpoints may expose sensitive infrastructure if unauthenticated or internet-accessible. <br>
Mitigation: Keep TrueNAS, Dockge, and related service endpoints on trusted networks, avoid internet exposure, and use authentication where supported. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anotb/truenas-skill) <br>
- [App Installation Guide](references/app-installation.md) <br>
- [Media Management](references/media-management.md) <br>
- [Downloads](references/downloads.md) <br>
- [Homelab Services](references/homelab-services.md) <br>
- [Books and Media](references/books-and-media.md) <br>
- [Bookmarks](references/bookmarks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Node.js helper scripts that return JSON from configured TrueNAS or Dockge endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, skill metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
