## Description: <br>
Vmware Harden helps agents perform VMware compliance auditing, baseline checking, drift detection, remediation-advice review, and compliance reporting for vSphere, ESXi, and NSX environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, infrastructure engineers, and compliance operators use this skill to scan VMware estates against built-in or custom baselines, inspect violations and drift, and obtain remediation advice before any approved change workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is mostly read-oriented, but its documentation describes remediation advice that can lead to real infrastructure changes through vmware-pilot. <br>
Mitigation: Review findings and proposed remediation plans before production use, and keep remediation execution explicitly approval-gated through vmware-pilot. <br>
Risk: If ANTHROPIC_API_KEY is enabled, compliance findings and infrastructure evidence may be sent to Anthropic for remediation advice. <br>
Mitigation: Enable ANTHROPIC_API_KEY only when organizational policy allows that data transfer; otherwise rely on the documented mock fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-harden) <br>
- [Publisher profile](https://clawhub.ai/user/zw008) <br>
- [Capabilities reference](references/capabilities.md) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Setup guide](references/setup-guide.md) <br>
- [Cross-skill workflows](references/cross-skill-workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured command guidance with optional JSON report references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local DuckDB state, VMware baseline identifiers, MCP tool outputs, and optional Anthropic-backed remediation suggestions.] <br>

## Skill Version(s): <br>
1.6.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
