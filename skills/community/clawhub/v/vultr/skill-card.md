## Description: <br>
Manage Vultr cloud infrastructure including VPS instances, bare metal, Kubernetes clusters, databases, DNS, firewalls, VPCs, object storage, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happytreees](https://clawhub.ai/user/happytreees) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to administer Vultr resources through the Vultr API, including compute, Kubernetes, databases, DNS, networking, storage, billing, tickets, and account users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad account and infrastructure changes in a Vultr account. <br>
Mitigation: Install it only when an agent is intended to administer Vultr, and use a narrowly scoped API key where possible. <br>
Risk: The API key grants access through a local credential file. <br>
Mitigation: Protect ~/.config/vultr/api_key with restrictive file permissions and avoid production-wide credentials. <br>
Risk: Delete, reinstall, user-management, DNS, firewall, storage, Kubernetes, database, billing, ticket, and key-regeneration actions can be destructive or account-changing. <br>
Mitigation: Require explicit human review before executing those actions. <br>


## Reference(s): <br>
- [Vultr API Reference](references/api-reference.md) <br>
- [Vultr API v2 Endpoint](https://api.vultr.com/v2) <br>
- [ClawHub Skill Page](https://clawhub.ai/happytreees/vultr) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, API calls, Configuration, Guidance] <br>
**Output Format:** [JSON responses and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Vultr API key stored at ~/.config/vultr/api_key.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
