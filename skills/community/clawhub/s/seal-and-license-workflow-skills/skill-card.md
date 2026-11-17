## Description:

For script sales and local delivery scenarios, this skill guides users in sealing Python script collections into source-bound local packages with MGC 1.5.4 or later.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to package and distribute Python workflows for customer delivery, with node-specific licensing or public free-mode distribution through MGC. It provides setup guidance and examples for sealing, importing, and running those packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Re-importing a package on the same node with the same info_owner can overwrite the original source records irreversibly.

Mitigation: Keep a source backup and use a different info_owner or a separate node before importing.

Risk: Sealed scripts still run code from the package author, and the bundled examples write files to Desktop or the home directory.

Mitigation: Trust the author and MGC runtime before execution, and protect existing files at the example output locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zkeviny/skills/seal-and-license-workflow-skills)
- [MGC Blackbox repository](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox issues](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown instructions with Python/MGC examples, shell commands, and package file layouts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover workflow sealing, package import, and execution; MGC 1.5.4 or later is required.]

## Skill Version(s):

1.3.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
