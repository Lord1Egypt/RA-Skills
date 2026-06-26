## Description: <br>
Generates complete two-sample Mendelian randomization study designs with four workload plans, workflow steps, validation strategy, risk review, and publication upgrade guidance from user-specified exposures and outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theresayao0614-sudo](https://clawhub.ai/user/theresayao0614-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External biomedical researchers, analysts, and agent users use this skill to plan two-sample MR studies from exposure-outcome research questions. It helps structure GWAS source selection, instrument screening, sensitivity analysis, figure planning, and publication upgrades while keeping assumptions explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat biomedical research-planning output as medical advice or as proof of causality. <br>
Mitigation: Use the skill as research-planning assistance only, and require domain expert review before acting on study conclusions. <br>
Risk: Ancestry mismatch, unsuitable GWAS sources, or sample overlap can bias two-sample MR designs. <br>
Mitigation: Verify ancestry matching, GWAS source suitability, and sample overlap against the actual study population and data access before analysis. <br>
Risk: Example R code and GWAS identifiers may not fit the user's actual phenotype or data-access context. <br>
Mitigation: Replace example identifiers, confirm availability in the selected GWAS source, and review the code before execution. <br>


## Reference(s): <br>
- [GWAS Database Recommendations by Exposure Class](references/gwas_databases.md) <br>
- [IV Count Benchmarks and Weak-Instrument Risk](references/iv_benchmarks.md) <br>
- [IEU Open GWAS](https://gwas.mrcieu.ac.uk) <br>
- [ClawHub Skill Page](https://clawhub.ai/theresayao0614-sudo/two-sample-mr-research-planner-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown research plan with optional R code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Lite, Standard, Advanced, and Publication+ configurations, a recommended plan, validation strategy, risk review, figure plan, minimal executable version, and publication upgrade path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
