## Description:

Generate VASP DFT calculation input files (INCAR, KPOINTS, POSCAR, POTCAR) for structural optimization, electronic structure, molecular dynamics, band structure, and density-of-states workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runye](https://clawhub.ai/user/runye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational materials scientists use this skill to generate and review VASP input files for DFT calculations, including relaxation, static, molecular dynamics, band structure, and density-of-states workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files can overwrite existing VASP input files in the selected output directory.

Mitigation: Run the generator in a working folder or back up existing INCAR and KPOINTS files before execution.

Risk: Default calculation parameters may not match a specific material, pseudopotential set, or production accuracy requirement.

Mitigation: Review ENCUT, k-point density, smearing, spin settings, and POTCAR choices before using generated inputs for VASP calculations.

## Reference(s):

- [VASP INCAR Parameters Reference](references/incar-parameters.md)
- [ClawHub Skill Page](https://clawhub.ai/runye/skills/vasp-input-generator)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with generated VASP text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local INCAR, KPOINTS, and optional POSCAR.template files; POTCAR generation remains guidance only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
