## Description: <br>
A comprehensive skill for Tencent EdgeOne (Edge Security & Acceleration Platform), covering edge acceleration, edge security, edge media, edge development, and EdgeOne operations through Tencent Cloud APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure, query, and troubleshoot Tencent EdgeOne sites, acceleration, certificates, security policies, observability workflows, and API operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use Tencent Cloud CLI with access to a Tencent Cloud or EdgeOne account, including operations with financial, security, or service-impacting consequences. <br>
Mitigation: Require explicit user confirmation before every write, purchase, certificate deployment, cache purge, IP blocklist change, package upgrade, or CAM service-linked role creation. <br>
Risk: Vague troubleshooting requests can lead to actions against the wrong EdgeOne account, zone, domain, or time range. <br>
Mitigation: Confirm the target account, zone, domain, time range, and intended action before making API calls or proposing operational changes. <br>
Risk: The security scan reports under-disclosed automatic account and local-environment changes. <br>
Mitigation: Review the skill before installation and only run it in environments where Tencent Cloud credentials and local CLI changes are acceptable. <br>


## Reference(s): <br>
- [Tencent EdgeOne Homepage](https://edgeone.ai) <br>
- [Tencent EdgeOne Product Documentation](https://edgeone.ai/document) <br>
- [ClawHub Skill Page](https://clawhub.ai/tencent-adm/tencent-edgeone-skill) <br>
- [API Reference](references/api/README.md) <br>
- [Acceleration Reference](references/acceleration/README.md) <br>
- [Security Reference](references/security/README.md) <br>
- [Observability Reference](references/observability/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, API parameters, tables, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Tencent Cloud CLI command proposals and scripts for EdgeOne operations.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
