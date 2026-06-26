## Description: <br>
Generates Kaplan-Meier survival curves, survival statistics, and hazard ratio estimates for clinical and biological time-to-event data analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Biomedical researchers, clinicians, and data analysts use this skill to run local Kaplan-Meier survival analysis on CSV time-to-event datasets and produce curves, statistical summaries, hazard ratios, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical datasets and generated plots, CSV summaries, or reports may expose sensitive clinical information or derived statistics. <br>
Mitigation: Use de-identified or authorized datasets only, and review all generated outputs before sharing. <br>
Risk: The script reads local input paths and writes analysis files to a user-selected output directory. <br>
Mitigation: Install and run the skill in an isolated Python environment, and direct outputs to a dedicated workspace folder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/survival-analysis-km) <br>
- [Publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>
- [References and Resources for Survival Analysis](references/README.md) <br>
- [Sample survival dataset](references/sample_data.csv) <br>
- [lifelines documentation](https://lifelines.readthedocs.io/) <br>
- [scikit-survival documentation](https://scikit-survival.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Markdown guidance with bash command examples; generated artifacts include PNG, PDF, CSV, and TXT files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-provided CSV and writes results to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
