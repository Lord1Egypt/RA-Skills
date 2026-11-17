## Description:

Automates a local Windows SOLIDWORKS installation through the official COM API to create parametric parts, assemblies, drawings, batch exports, mass and feature inspection, and preview renders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjh-ux](https://clawhub.ai/user/wjh-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CAD automation engineers use this skill to generate or modify SOLIDWORKS parts, assemblies, and drawings, then export CAD deliverables through scripts instead of direct GUI control. It is intended for Windows machines with SOLIDWORKS installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation scripts can close open SOLIDWORKS documents before running.

Mitigation: Save and close unrelated SOLIDWORKS work before use, or remove the close_all calls when adapting scripts for production workflows.

Risk: Generated CAD files and exports may overwrite existing files in the script output directory.

Mitigation: Run examples in a scratch directory or on copied CAD files, and add backup or unique-output naming before batch or production use.

Risk: The skill depends on local Windows COM automation and a compatible SOLIDWORKS installation.

Mitigation: Verify SOLIDWORKS, pywin32, templates, and version-specific COM type library settings on the target workstation before relying on generated output.

## Reference(s):

- [SOLIDWORKS API Patterns](references/api-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/wjh-ux/skills/solidworks-modeling)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or modify SOLIDWORKS CAD files and exports when run on a configured Windows workstation.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
