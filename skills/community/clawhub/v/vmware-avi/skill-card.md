## Description: <br>
VMware AVI helps agents manage AVI/NSX Advanced Load Balancer virtual services, pool members, SSL checks, analytics, service engine health, and AKO Kubernetes troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Platform engineers, SREs, and developers use this skill to inspect and administer VMware AVI/NSX ALB load balancing and AKO ingress environments, including traffic-affecting maintenance workflows and diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can administer live AVI/NSX ALB and AKO environments, including actions that affect application traffic. <br>
Mitigation: Install it only for intended infrastructure operators, use least-privilege AVI and Kubernetes accounts, and require reviewers to inspect confirmation prompts before traffic-affecting actions. <br>
Risk: Controller passwords and Kubernetes access may expose sensitive infrastructure if stored or handled casually. <br>
Mitigation: Prefer a secret manager over plaintext .env files, avoid entering passwords in shell commands, and keep credential files restricted to authorized users. <br>
Risk: Disabling TLS verification can hide controller impersonation or interception in production environments. <br>
Mitigation: Keep TLS verification enabled for production and use valid controller certificates. <br>


## Reference(s): <br>
- [VMware AVI ClawHub Skill Page](https://clawhub.ai/zw008/skills/vmware-avi) <br>
- [VMware AVI project homepage](https://github.com/zw008/VMware-AVI) <br>
- [VMware AVI Capabilities](references/capabilities.md) <br>
- [VMware AVI CLI Reference](references/cli-reference.md) <br>
- [VMware AVI Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, analysis] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke CLI or MCP tools that inspect or modify AVI Controller and Kubernetes AKO resources when the user has configured credentials and approved write actions.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
