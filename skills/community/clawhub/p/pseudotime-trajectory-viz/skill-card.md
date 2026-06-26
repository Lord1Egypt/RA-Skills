## Description: <br>
Analyze single-cell AnnData files with a reproducible pseudotime trajectory workflow that validates inputs and produces review-ready visualizations and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and computational biology teams use this skill to infer developmental trajectories, calculate pseudotime, visualize lineage branching, and inspect gene expression dynamics from preprocessed single-cell AnnData files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CSV, JSON, plots, and AnnData files may include cell IDs, annotations, or sample-derived metadata. <br>
Mitigation: Send outputs to a controlled directory and review generated artifacts before sharing. <br>
Risk: Automatically inferred roots, lineages, and pseudotime values are exploratory biological results. <br>
Mitigation: Validate trajectories against marker genes, biological knowledge, and alternate methods before relying on conclusions. <br>
Risk: The skill reads local AnnData files and writes local analysis results. <br>
Mitigation: Install dependencies in an isolated Python environment and use only datasets you are authorized to analyze. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/pseudotime-trajectory-viz) <br>
- [Runtime checklist](references/runtime_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local output files including plots, CSV, JSON, and AnnData artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces trajectory plots, pseudotime values, analysis reports, and updated AnnData files in a user-controlled output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
