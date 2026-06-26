## Description: <br>
Vmware Policy provides unified audit logging, policy rule enforcement, and input sanitization for VMware MCP skill-family workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and VMware operators use this skill to query audit logs, export audit records, manage local policy rules, and integrate shared audit and sanitization helpers into VMware MCP skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy enforcement can be bypassed globally with VMWARE_POLICY_DISABLED, which can disable protections across VMware skill-family operations. <br>
Mitigation: Restrict who can set that environment variable, monitor audit entries with bypass status, and do not treat this skill as the only control for high-risk VMware operations. <br>
Risk: Fail-open defaults can allow operations when policy rules are absent or supporting dependencies are unavailable. <br>
Mitigation: Create and protect ~/.vmware/rules.yaml before production use, validate the rules file, and verify denied-operation logging before relying on policy enforcement. <br>
Risk: Local audit databases and exported JSON logs may contain operational details about VMware environments. <br>
Mitigation: Secure ~/.vmware/audit.db and exported logs with appropriate filesystem permissions and handle exports as sensitive operational records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-policy) <br>
- [Project homepage from metadata](https://github.com/zw008/VMware-Policy) <br>
- [Capabilities reference](artifact/references/capabilities.md) <br>
- [CLI reference](artifact/references/cli-reference.md) <br>
- [Setup guide](artifact/references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, YAML configuration, and CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audit-query and policy-configuration guidance; it does not expose MCP tools directly.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
