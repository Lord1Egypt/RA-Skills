## Description: <br>
Analyze Redis Sentinel and Cluster configurations for high availability, performance, and memory efficiency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to audit Redis, Sentinel, or Cluster deployments, review configuration and application connection code, and prioritize production-readiness fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redis configuration files and command output can expose sensitive operational details such as passwords, connection strings, hostnames, and internal IPs. <br>
Mitigation: Provide only intended Redis or project paths and ask the agent to redact secrets and infrastructure identifiers from reports. <br>
Risk: Runtime redis-cli checks can query the wrong environment if scope is ambiguous. <br>
Mitigation: Confirm the target host, context, and environment before allowing any redis-cli checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/redis-cluster-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with findings, scores, topology summaries, remediation directives, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Redis health scores, category scores, priority matrices, and exact redis.conf remediation snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
