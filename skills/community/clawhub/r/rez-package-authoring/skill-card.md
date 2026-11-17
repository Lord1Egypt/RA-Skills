## Description:

Guides developers in authoring and reviewing Rez package.py files, including version and variant choices, dependency ranges, build requirements, and release workflows for Rez 3.4.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, review, or restructure Rez packages and to decide when changes need a new version or variant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a local Rez build can shadow an existing released package.

Mitigation: Inspect the resolved package and test the local build before relying on it.

Risk: Running rez-release can publish packages to shared repositories and tag the release.

Mitigation: Review the release destination and changes, and run package tests before publishing.

## Reference(s):

- [Rez Package Authoring on ClawHub](https://clawhub.ai/loonghao/skills/rez-package-authoring)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
