## Description:

Audits VMware vSphere, ESXi, and NSX environments against compliance baselines, checks known vulnerabilities and configuration drift, and provides remediation advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and VMware administrators use this skill to scan vSphere, ESXi, and NSX environments for compliance gaps, known vulnerabilities, and configuration drift, then review suggested remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags the remediation-advisor examples for not clearly warning that compliance context may be sent to an external provider; its scan was partial and some local references were unresolved.

Mitigation: Review the unresolved references and the advisor's data handling before installation; check what compliance context would be sent to Anthropic before enabling live advice.

## Reference(s):

- [Project homepage listed in skill metadata](https://github.com/vmware-skills/VMware-Harden)
- [Capabilities and tool behavior](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [STIG content sync notes](artifact/references/stig-content-sync.md)
- [MCP result contract](artifact/references/mcp-result-contract.md)

## Skill Output:

**Output Type(s):** [Markdown reports, JSON results, Shell commands, Configuration guidance, Remediation advice]

**Output Format:** [Markdown and JSON, with command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include compliance findings, scan coverage, vulnerability status, and drift details; remediation is advisory.]

## Skill Version(s):

1.20.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
