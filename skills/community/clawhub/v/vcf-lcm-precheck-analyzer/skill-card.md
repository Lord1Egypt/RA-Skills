## Description:

An MCP server that interfaces with VCF SDDC Manager to retrieve and analyze LCM upgrade pre-check results, providing instant remediation steps for failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasture-rohit](https://clawhub.ai/user/kasture-rohit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this MCP server with OpenClaw to retrieve the latest VMware Cloud Foundation LCM pre-check results from SDDC Manager and summarize failures, warnings, and remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an SDDC Manager API token over HTTPS while certificate verification is disabled.

Mitigation: Use a least-privilege, read-only SDDC Manager token, restrict outbound network access, and enable certificate verification or configure a trusted private CA bundle before production use.

Risk: Dependencies are not pinned in the artifact requirements file.

Mitigation: Pin dependency versions and review updates before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kasture-rohit/skills/vcf-lcm-precheck-analyzer)
- [Skill homepage](https://github.com/kasture-rohit/vcf-openclaw-skills)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns latest pre-check status, failure and warning details, remediation actions, or connection and configuration error messages.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
