## Description:

Generate an Xcode SF Symbol asset catalog .symbolset from an SVG. Use when you need to add a custom SF Symbol (build-time) by creating the symbolset folder, Contents.json, and SVG file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svkozak](https://clawhub.ai/user/svkozak)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create custom Xcode SF Symbol `.symbolset` assets from SVG inputs, including the symbolset directory, `Contents.json`, and SVG asset. It supports raw symbolset creation and template-based SVG injection for build-time asset catalog workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe symbol names or asset directory values can cause generated files to be written outside the intended Xcode asset folder.

Mitigation: Use trusted, simple SF Symbol names and known asset directories; add strict symbol-name validation and destination containment checks before broad automated use.

Risk: Automated or untrusted-input workflows could let issue text or repository data choose output paths.

Mitigation: Require human review for symbol-name and assets-dir values before execution in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/svkozak/skills/sfsymbol-generator)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation of Xcode asset catalog files; generated artifacts include `.symbolset` directories, SVG files, and `Contents.json` files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
