## Description:

Create parametric 3D models and prepare image-guided meshes or Bambu projects for Snapmaker U1 printing, with geometry, toolpath, color and print settings checks, plus optional local printer status and loaded-spool queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rahulbsw](https://clawhub.ai/user/rahulbsw)

### License/Terms of Use:

MIT

## Use Case:

Developers and makers use the skill to create or prepare 3D models and Snapmaker U1 projects, then review geometry, color, slicer output and optional read-only printer status before printing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence notes that the documented npx installation command is unpinned, so the package used can change between installs.

Mitigation: For reproducible installations, pin the skills CLI version where supported and review the resolved package before running it.

Risk: Security scan coverage is partial: one local reference was unresolved and some binary content was outside analyzer scope.

Mitigation: Review the unresolved reference and inspect binary assets before deployment.

Risk: Optional converters, model weights, runtimes, and external applications have separate terms; the Bambu conversion backend is noncommercial.

Mitigation: Check the applicable component and model terms before enabling optional workflows, especially for commercial use.

## Reference(s):

- [ClawHub release](https://clawhub.ai/rahulbsw/skills/snapmaker-u1-skill)
- [Source repository](https://github.com/rahulbsw/snapmaker-u1-skill)
- [Imported source commit](https://github.com/rahulbsw/snapmaker-u1-skill/commit/84546faf6885b5ebe0cda04b685d4f36460b2c2e)
- [Snapmaker U1 print guide](docs/PRINT_GUIDE.md)
- [Image reconstruction guidance](references/IMAGE_TO_3D.md)
- [Read-only printer check guidance](references/PRINTER_CHECK.md)
- [Snapmaker U1 documentation](https://wiki.snapmaker.com/en/snapmaker_u1)
- [Snapmaker OrcaSlicer](https://github.com/Snapmaker/OrcaSlicer)

## Skill Output:

**Output Type(s):** [3D model and project files, JSON reports, Markdown guidance, Shell commands]

**Output Format:** [STL and GLB meshes, 3MF projects, JSON review reports, and Markdown print notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available outputs depend on optional local engines, macOS tools, printer access, and slicer installations; workflows do not start a physical print.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
