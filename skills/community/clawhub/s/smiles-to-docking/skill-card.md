## Description: <br>
End-to-end virtual screening workflow: SMILES to 3D SDF, ligand/receptor preparation to PDBQT, batch AutoDock Vina docking, affinity ranking, and Top-N complex export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ning-kun](https://clawhub.ai/user/ning-kun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drug discovery researchers and computational chemistry developers use this skill to automate small-molecule virtual screening from SMILES input through docking, ranking, and top-complex export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted molecule filenames, ligand names, or output paths could cause unintended local command execution. <br>
Mitigation: Use trusted molecule files and safe ASCII names without shell metacharacters, run the workflow in an isolated conda or virtual environment, and prefer a patched version that sanitizes names and uses argument-list subprocess calls. <br>


## Reference(s): <br>
- [AutoDock Vina Parameter Guide](references/vina_param_guide.md) <br>
- [Pocket Estimation from Co-Crystallized Ligand](references/pocket_from_ligand.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, command-line examples, generated docking result files, CSV rankings, and exported PDB complexes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local chemistry and docking tools and writes staged output directories for molecule conversion, preparation, docking, and ranking.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
