## Description: <br>
爪爪分布式部署系统 —— 实现多实例协同、负载均衡、故障转移。Use when 爪爪需要分布式部署、多设备协同、或构建爪爪网络。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beipian261](https://clawhub.ai/user/beipian261) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill as a scaffold for planning distributed Zhua deployments across multiple devices, including master, compute, and storage instance roles. Treat the generated commands and configuration guidance as starting points that require review and completion before production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release advertises distributed deployment, synchronization, load balancing, and failover capabilities that are mostly not implemented or safely scoped in the artifacts. <br>
Mitigation: Review before installing and use only in a test environment unless node management, synchronization, authentication, rollback, and data-scope controls are added and verified. <br>


## Reference(s): <br>
- [API Reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run helper scripts that create local Zhua distributed instance configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
