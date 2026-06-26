## Description: <br>
Build, review, debug, and automate VASP first-principles workflows. Use when working with VASP input sets such as INCAR, POSCAR, KPOINTS, and POTCAR; when choosing SCF, relaxation, static, DOS, or band-structure stages; or when fixing convergence, symmetry, cutoff, and k-point issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fzj1214](https://clawhub.ai/user/fzj1214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and HPC users use this skill to prepare, review, and repair VASP input sets and staged workflows for relaxation, static SCF, DOS, and band-structure calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or copied Slurm launch scripts can be inappropriate for a specific cluster environment. <br>
Mitigation: Before execution, verify the VASP executable or module setup, task count, walltime, working directory, output paths, and site-specific scheduler requirements. <br>
Risk: VASP workflow guidance can be invalid if stage intent, restart files, species order, or POTCAR assumptions do not match the actual system. <br>
Mitigation: Review the four-file input set, stage handoff files, and pseudopotential order before production runs or downstream DOS and band-structure analysis. <br>


## Reference(s): <br>
- [VASP Input Set Manual](references/input-set-manual.md) <br>
- [VASP Stage And Parameter Matrix](references/stage-and-parameter-matrix.md) <br>
- [VASP Pseudopotential, K-Points, And Convergence](references/pseudopotential-kpoints-and-convergence.md) <br>
- [VASP Cluster Execution Playbook](references/cluster-execution-playbook.md) <br>
- [VASP Error Recovery](references/error-recovery.md) <br>
- [VASP DOS And Band Workflows](references/dos-and-band-workflows.md) <br>
- [VASP Workflow Handoff Matrix](references/workflow-handoff-matrix.md) <br>
- [VASP Error Pattern Dictionary](references/error-pattern-dictionary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, command snippets, configuration examples, and workflow summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize workflow stage, INCAR intent, KPOINTS strategy, POTCAR and species assumptions, expected outputs, and next-stage handoff guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
