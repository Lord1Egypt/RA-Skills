## Description: <br>
Routes Volcano Engine Serverless Flink requests to domain-specific subskills for CLI setup, project and configuration management, resources, connectors, job development, operations, monitoring, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvheyang](https://clawhub.ai/user/lvheyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and data platform engineers use this skill to administer Volcano Engine Serverless Flink through `volc_flink`, including setup, project selection, SQL, JAR, CDC job workflows, operations, monitoring, and diagnostics. <br>

### Deployment Geography for Use: <br>
Volcano Engine supported regions: cn-beijing, cn-shanghai, cn-guangzhou, and ap-singapore. <br>

## Known Risks and Mitigations: <br>
Risk: Credential-sensitive workflows may expose Volcano Engine access keys, secret keys, endpoints, or message payloads. <br>
Mitigation: Use least-privilege credentials, prefer interactive or managed secret flows, redact sensitive output, and do not paste secrets into chat, SQL, YAML, or command examples. <br>
Risk: The skill can guide create, update, delete, stop, restart, rescale, restore, and publish actions that affect running Flink resources. <br>
Mitigation: Review each proposed command, resolve the exact target object, require explicit confirmation before state changes, and verify the result after execution. <br>
Risk: Kafka sampling or log inspection may reveal confidential business data. <br>
Mitigation: Avoid raw payload output unless the user has confirmed the data is safe to display, and summarize or redact sensitive values where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvheyang/volc-flink-skill) <br>
- [Integrated skill overview](artifact/README.md) <br>
- [Root routing skill](artifact/SKILL.md) <br>
- [Security conventions](artifact/COMMON_SECURITY.md) <br>
- [Mutation conventions](artifact/COMMON_MUTATION.md) <br>
- [CDC volc_flink command reference](artifact/skills/flink-cdc/references/volc_flink_commands.md) <br>
- [SQL volc_flink command reference](artifact/skills/flink-sql/references/volc_flink_commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, SQL, YAML, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose read-only checks, change plans, and guarded execution steps that require user confirmation for state-changing operations.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
