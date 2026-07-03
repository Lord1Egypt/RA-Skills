## Description: <br>
Use this skill for VMware compliance auditing, baseline checking, and drift detection across vSphere, ESXi, and NSX environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, infrastructure engineers, and security operators use this skill to run VMware compliance scans, evaluate built-in or custom baselines, inspect violations, review drift, and generate remediation advice without directly applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remediation apply behavior could cause real VMware changes if an agent follows inconsistent documentation without approval controls. <br>
Mitigation: Use the skill for scanning, reporting, and advice only; require vmware-pilot approval gates and audit logging before any remediation execution. <br>
Risk: The local DuckDB and audit files may contain sensitive infrastructure evidence. <br>
Mitigation: Store and share the DuckDB and audit logs as sensitive operational data with appropriate access controls. <br>
Risk: Setting ANTHROPIC_API_KEY may send violation details to Anthropic for remediation advice. <br>
Mitigation: Enable the API key only after confirming that external processing of violation details is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [Capabilities](references/capabilities.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Cross-Skill Workflows](references/cross-skill-workflows.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zw008/skills/vmware-harden) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured compliance findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can reference local DuckDB evidence, compliance baseline identifiers, JSON reports, drift summaries, and approval-gated remediation guidance.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
