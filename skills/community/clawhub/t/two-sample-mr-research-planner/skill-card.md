## Description: <br>
Generates two-sample Mendelian randomization research designs with four workload options, a recommended plan, workflow, validation strategy, figure plan, and publication upgrade path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanruoyu](https://clawhub.ai/user/shanruoyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and analysts use this skill to plan two-sample Mendelian randomization studies from an exposure-outcome research direction. It structures feasible study designs, sensitivity checks, figure plans, validation steps, and publication upgrade paths using GWAS summary statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research plans may be mistaken for validated statistical or medical advice. <br>
Mitigation: Treat outputs as research-planning guidance and require domain review before using them to make scientific, clinical, or publication claims. <br>
Risk: Two-sample MR validity can be undermined by ancestry mismatch, sample overlap, weak instruments, or unsuitable GWAS sources. <br>
Mitigation: Check ancestry matching, overlap status, instrument strength, and GWAS suitability before running or interpreting the proposed analysis. <br>


## Reference(s): <br>
- [GWAS Database Recommendations by Exposure Class](references/gwas_databases.md) <br>
- [IV Count Benchmarks and Weak-Instrument Risk by Exposure Class](references/iv_benchmarks.md) <br>
- [IEU Open GWAS](https://gwas.mrcieu.ac.uk) <br>
- [ClawHub skill page](https://clawhub.ai/shanruoyu/two-sample-mr-research-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with optional R code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Always includes Lite, Standard, Advanced, and Publication+ configurations plus a recommended primary plan.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
