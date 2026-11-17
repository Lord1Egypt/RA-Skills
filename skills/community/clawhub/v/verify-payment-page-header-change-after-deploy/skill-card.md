## Description:

Verifies deployed payment-page HTTP security headers and produces dated evidence for authorization review after deployment changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and compliance reviewers use this skill to verify live payment-page security headers after a deployment, compare captured headers with an approved baseline, and retain authorization evidence for PCI DSS v4.0.1 Requirement 11.6.1 workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an unpinned third-party install command.

Mitigation: Review and preferably pin the installer, package, or source before running the npx install command.

Risk: The MCP check sends the target URL to a third-party service.

Mitigation: Use the check only for public payment-page URLs intended to be shared with PowMCP.

Risk: A header score or presence report could be mistaken for PCI compliance or authorization evidence.

Mitigation: Require the approved baseline, full capture or diff, review decision, and retained records before making an authorization conclusion.

## Reference(s):

- [Security Headers Check reference](references/security-headers-check.md)
- [Security Headers Check app page](https://powmcp.com/apps/security-headers-check/)
- [PCI DSS payment-page requirements](https://cside.com/blog/pci-dss-4-0-1-requirements-6-4-3-11-6-1-client-side-compliance-guide)
- [PCI DSS v4.0.1 implementation](https://www.sikich.com/insight/preparing-for-pci-dss-v4-0-1-requirements-6-4-3-and-11-6-1/)
- [Payment-page compliance workflow](https://jscrambler.com/blog/pci-dss-4-0-1/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with checklist items, evidence fields, findings table, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dated live-response observations, raw header capture guidance, baseline diff disposition, authorization review status, and unassessable evidence gaps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
