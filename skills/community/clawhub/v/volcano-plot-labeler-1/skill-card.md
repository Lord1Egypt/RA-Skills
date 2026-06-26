## Description: <br>
Automatically labels the top significant genes in volcano plots from CSV or TSV differential-expression data and writes a labeled plot image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and data analysts use this skill to generate volcano plots from differential-expression tables, highlight top genes, and produce reviewable plot files for reports or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local CSV or TSV input and writes a plot file to the output path supplied by the user. <br>
Mitigation: Run it in a sandboxed workspace, validate input and output paths, and process only files intended for this analysis. <br>
Risk: Python dependencies are declared without pinned versions. <br>
Mitigation: Pin or review dependency versions before repeatable or shared use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/volcano-plot-labeler-1) <br>
- [Runtime Checklist](references/runtime_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with Python examples and local plot files such as PNG, PDF, or SVG] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local CSV or TSV input and writes the requested plot file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
