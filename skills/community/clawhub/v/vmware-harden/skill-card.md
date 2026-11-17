## Description:

Audits VMware vSphere, ESXi, and NSX environments against security baselines, checks known advisories, detects configuration drift, and provides remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

VMware administrators and security or compliance engineers use this skill to assess vSphere, ESXi, and NSX configurations against supported baselines, review known vulnerabilities and drift, and evaluate suggested remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Results can be incomplete when collectors lack coverage or per-node evidence is missing.

Mitigation: Review coverage and undetermined checks; do not treat an empty violations list as proof of compliance.

Risk: Known-vulnerability results are limited to the offline catalog date, and unknown builds are not passes.

Mitigation: Check the catalog date and verify unknown or newer cases against current Broadcom advisories.

Risk: Suggested remediation may be unsuitable for a particular environment.

Mitigation: Review suggestions and route any changes through the approval-gated vmware-pilot workflow.

Risk: Setup examples include Docker or uvx usage without pinned versions, and the security scan reports partial analysis coverage.

Mitigation: Pin deployment dependencies where reproducibility matters and review unresolved references before relying on scan conclusions.

## Reference(s):

- [VMware Harden on ClawHub](https://clawhub.ai/zw008/skills/vmware-harden)
- [VMware Harden project homepage](https://github.com/vmware-skills/VMware-Harden)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance]

**Output Format:** [Text, Markdown, JSON, and CSV reports, plus structured MCP results and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Point-in-time findings; review coverage and unknown results. Remediation suggestions are advisory.]

## Skill Version(s):

1.20.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
