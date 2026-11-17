## Description:

Guides agents through making a local copy of a website for offline study or authorized reuse while preserving page structure, visual assets, and basic interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alps9999](https://clawhub.ai/user/alps9999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect a target site's resources, download HTML, CSS, JavaScript, images, fonts, and data files, adapt them for local serving, and verify visual fidelity. It is most appropriate for sites the user owns or has permission to copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can be used to copy websites or replace attribution without authorization.

Mitigation: Use it only for sites you own or have permission to copy, and preserve attribution unless you are authorized to change it.

Risk: Shell examples that interpolate target URLs can behave unexpectedly when given malformed or untrusted input.

Mitigation: Validate and quote target URLs before running commands, and run the workflow in a limited workspace.

Risk: The artifact demonstrates unpinned remote package execution through browser automation commands.

Mitigation: Pin or preinstall browser automation dependencies before use instead of running an @latest package directly.

Risk: Website downloads and local serving can expose local files or credentials if run from a sensitive directory.

Mitigation: Run the workflow in a clean workspace that does not contain secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alps9999/skills/website-cloner)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local validation and troubleshooting checklists for static website copies.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
