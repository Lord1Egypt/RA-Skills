## Description: <br>
Generate VASP input files (INCAR, KPOINTS, POSCAR.template) for DFT tasks like relaxation, static calculations, molecular dynamics, band structure, and density of states calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Runye](https://clawhub.ai/user/Runye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computational materials researchers use this skill to create and review starter VASP calculation inputs for common DFT workflows. It helps draft INCAR, KPOINTS, and POSCAR template content while reminding users to generate POTCAR separately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated VASP parameters may be unsuitable for a specific material system or calculation objective. <br>
Mitigation: Review INCAR, KPOINTS, and POSCAR.template content against the target structure, pseudopotentials, and convergence requirements before spending compute. <br>
Risk: Running the generator in an active calculation directory can overwrite intended INCAR, KPOINTS, or POSCAR.template files. <br>
Mitigation: Run the generator only in a new or intended VASP calculation directory and keep backups of existing input files. <br>


## Reference(s): <br>
- [VASP INCAR Parameters Reference](references/incar-parameters.md) <br>
- [ClawHub release page](https://clawhub.ai/Runye/vasp-input-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated VASP input-file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local INCAR, KPOINTS, and POSCAR.template files when its bundled generator script is run; POTCAR is guidance only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
