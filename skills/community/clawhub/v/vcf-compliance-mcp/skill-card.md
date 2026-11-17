## Description:

An MCP server that interfaces with VMware Aria Operations to run regulatory compliance checks (ISO 27001, PCI DSS, CIS, etc.) against the VCF environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasture-rohit](https://clawhub.ai/user/kasture-rohit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure security engineers use this skill to let an agent query VMware Aria Operations for VCF compliance alerts and summarize status against common regulatory benchmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Infrastructure API token misuse or overbroad access could expose sensitive environment data.

Mitigation: Use a narrowly scoped read-only Aria Operations token and rotate it according to the deployment owner's credential policy.

Risk: TLS certificate verification is disabled in the artifact server code.

Mitigation: Require normal TLS validation or configure a trusted CA bundle before production use.

Risk: When live API checks fail, the tool can return simulated compliance findings that may be mistaken for real audit data.

Mitigation: Remove the simulated fallback or clearly gate it behind an explicit test/demo mode before relying on outputs.

Risk: Dependencies are unpinned.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kasture-rohit/skills/vcf-compliance-mcp)
- [Project homepage](https://github.com/kasture-rohit/vcf-openclaw-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text returned from an MCP tool call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The compliance standard argument selects ISO, PCI, CIS, HIPAA, DISA, or FISMA.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
