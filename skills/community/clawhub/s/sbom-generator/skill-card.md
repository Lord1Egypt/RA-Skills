## Description:

Generate Software Bill of Materials (SBOM) in CycloneDX or SPDX format to inventory dependencies, licenses, vulnerabilities, and supply chain metadata for compliance and security audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and compliance reviewers use this skill to generate SBOM inventories, license reports, vulnerability summaries, SBOM diffs, and policy checks for software projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads dependency and lock files in the target project.

Mitigation: Run it only in repositories where the agent is allowed to inspect dependency metadata.

Risk: Optional audit commands may contact external package or vulnerability services using the environment's registry configuration.

Mitigation: Review registry and authentication settings before running audit steps, especially in private repositories.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JSON, CSV, and report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce CycloneDX JSON, SPDX JSON, CSV dependency inventories, Markdown license reports, SBOM diffs, and license policy configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
