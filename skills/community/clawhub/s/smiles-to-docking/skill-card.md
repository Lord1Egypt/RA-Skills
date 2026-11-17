## Description:

End-to-end virtual screening workflow: SMILES to 3D SDF, ligand/receptor preparation to PDBQT, batch AutoDock Vina docking, affinity ranking, and Top-N complex export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ning-kun](https://clawhub.ai/user/ning-kun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry teams use this skill to automate small-molecule virtual screening from SMILES libraries against protein receptor structures, including molecule preparation, docking, affinity ranking, and top-complex export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted ligand names or paths could trigger shell command execution or write files outside the intended output directory.

Mitigation: Install and run the skill in an isolated environment, and use only trusted SMILES files, ligand/input filenames, and output paths until shell command handling and filename validation are fixed.

Risk: Shared or sensitive directories could expose unintended files or make generated docking outputs hard to trust.

Mitigation: Use a dedicated non-sensitive working directory and review generated docking-result files before using or sharing them.

## Reference(s):

- [AutoDock Vina Parameter Guide](references/vina_param_guide.md)
- [Pocket estimation from a co-crystallized ligand](references/pocket_from_ligand.py)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Analysis]

**Output Format:** [Markdown guidance with bash commands plus generated CSV, TXT, SDF, PDBQT, PDB, and Vina log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes docking results under the requested output directory, including ranked scores and top-N complex exports.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
