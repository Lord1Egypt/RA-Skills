## Description: <br>
Automatically label top significant genes in volcano plots with a repulsion algorithm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EC-cyber258](https://clawhub.ai/user/EC-cyber258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics analysts use this skill to generate volcano plots from differential expression CSV or TSV data, automatically ranking and labeling the most significant genes while reducing label overlap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned Python dependencies may change behavior or introduce supply-chain risk. <br>
Mitigation: Pin or review dependency versions in requirements.txt and install in a trusted environment before use. <br>
Risk: The skill reads local input files and writes plot outputs in the workspace. <br>
Mitigation: Run it in a workspace-scoped environment and review input and output paths before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EC-cyber258/volcano-plot-labeler) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Plotting script](artifact/scripts/main.py) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Python API usage, shell commands, and generated plot image files such as PNG, PDF, or SVG] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local CSV or TSV differential expression data and writes plot files to the requested output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
