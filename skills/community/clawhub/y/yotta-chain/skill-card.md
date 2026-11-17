## Description:

Checks npm, Python, and Maven dependency manifests and lockfiles for supply-chain warning signs, and generates a CycloneDX 1.5 subset SBOM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use it before builds, releases, or CI to inspect authorized local projects for dependency and lockfile risks and create an SBOM. Findings are signals for human review, and the tool does not perform online CVE checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project files can trigger reads outside the selected folder when scanning untrusted repositories.

Mitigation: Run scans of untrusted repositories in isolation and make only intended project files readable until include-path containment is fixed.

Risk: Reports may expose sensitive values.

Mitigation: Remove credentials from registry URLs and keep reports private.

Risk: The packaged test suite is absent, so its advertised results could not be verified.

Mitigation: Prefer a reviewed, pinned release and one installation destination.

## Reference(s):

- [Dependency detection rules](references/rules.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, CSV]

**Output Format:** [Text, JSON, or CSV scan reports; text or CycloneDX 1.5 subset JSON SBOM]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only local analysis; findings are risk signals for human review.]

## Skill Version(s):

0.1.7 (source: ClawHub release, SKILL.md, CHANGELOG.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
