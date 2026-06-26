## Description: <br>
Uses the official UCloud CLI to inspect, create, update, or delete UCloud resources and plan web application deployments on UCloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingming-cn](https://clawhub.ai/user/mingming-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage real UCloud resources through CLI profiles, OAuth authorization, product subcommands, and API fallback calls. It supports read-only discovery, deployment planning, and controlled resource changes for UHost, networking, EIP, load balancing, databases, regions, zones, and projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real UCloud resource operations, including changes that may create cost, expose services, or alter existing infrastructure. <br>
Mitigation: Use it only for intended UCloud operations; confirm profile, region, resource names, cost impact, firewall exposure, and teardown steps before write or delete actions. <br>
Risk: Credential or token material could be exposed through chat, command previews, CLI output, or logs. <br>
Mitigation: Prefer OAuth or scoped existing profiles, avoid pasting AK/SK values into chat or commands, mask sensitive profile output, and use secure secret delivery for credentials. <br>
Risk: Broad deployment wording may cause the skill to activate for high-impact cloud planning and deployment requests. <br>
Mitigation: Start with read-only discovery and explicit deployment planning, then require user confirmation for concrete resource creation, network exposure, or deletion. <br>


## Reference(s): <br>
- [UCloud CLI Quick Start](https://docs.ucloud.cn/cli/intro) <br>
- [UCloud CLI Repository](https://github.com/ucloud/ucloud-cli) <br>
- [UCloud API Documentation](https://github.com/UCloudDoc-Team/api) <br>
- [UCloud Product Documentation](https://docs.ucloud.cn/) <br>
- [CLI Usage](references/cli-usage.md) <br>
- [Documentation Sources](references/doc-sources.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Deployment Defaults](references/deployment.md) <br>
- [Common Lookup API](references/common-lookups.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with CLI command examples, tables, and structured request or response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include UCloud CLI commands, temporary JSON payload guidance, masked credential handling, and next-step recommendations.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
