## Description:

Build, review, debug, and automate VASP first-principles workflows for input sets, staged calculations, convergence issues, and cluster execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fzj1214](https://clawhub.ai/user/fzj1214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and researchers use this skill to prepare, review, debug, and hand off VASP workflows across relaxation, static SCF, DOS, and band-structure stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied VASP inputs and Slurm settings may be unsuitable for a specific material system or cluster environment.

Mitigation: Review INCAR, POSCAR, KPOINTS, and POTCAR consistency; confirm POTCAR/species order, module or executable names, and scheduler resource requests before cluster use.

Risk: Restart and handoff decisions may accidentally carry stale WAVECAR, CHGCAR, CONTCAR, or related stage files into a later workflow step.

Mitigation: Keep stage directories explicit, preserve the last good outputs before overwriting, and make restart-file reuse a user-directed decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fzj1214/skills/vasp-skills)
- [VASP Input Set Manual](references/input-set-manual.md)
- [VASP Stage And Parameter Matrix](references/stage-and-parameter-matrix.md)
- [VASP Pseudopotential, K-Points, And Convergence](references/pseudopotential-kpoints-and-convergence.md)
- [VASP Cluster Execution Playbook](references/cluster-execution-playbook.md)
- [VASP Error Recovery](references/error-recovery.md)
- [VASP DOS And Band Workflows](references/dos-and-band-workflows.md)
- [VASP INCAR Tag Matrix](references/incar-tag-matrix.md)
- [VASP Workflow Handoff Matrix](references/workflow-handoff-matrix.md)
- [VASP Error Pattern Dictionary](references/error-pattern-dictionary.md)
- [VASP POSCAR, Species, And Structure Manual](references/poscar-species-and-structure.md)
- [VASP Restarts, Spin, And Wavefunction Files](references/restarts-spin-and-wavefunction-files.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with VASP input snippets, workflow summaries, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference reusable INCAR, KPOINTS, POSCAR, and Slurm template files when a concrete starting point is needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
