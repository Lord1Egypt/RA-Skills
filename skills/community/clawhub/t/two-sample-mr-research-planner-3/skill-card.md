## Description: <br>
Generates complete two-sample Mendelian randomization (MR) research designs from a user-provided exposure-outcome research direction, including four workload configurations, a recommended plan, workflow, figures, validation strategy, minimal version, and publication upgrade path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, analysts, and agent users use this skill to turn an MR causal research question into a structured two-sample Mendelian randomization study plan with workload options, sensitivity checks, figure planning, and R code scaffolding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide controlled-access, participant-level, proprietary, or identifiable genetic or health data while asking for an MR plan. <br>
Mitigation: Use public summary-level or otherwise permitted inputs only, and check data-use agreements and ethics approvals before sharing study details. <br>
Risk: Generated study plans, GWAS source choices, and R code scaffolds may be inappropriate for a specific dataset, ancestry, instrument strength, or publication target. <br>
Mitigation: Have a domain expert verify GWAS IDs, assumptions, instrument strength, sensitivity analyses, and code before relying on the plan. <br>


## Reference(s): <br>
- [GWAS Database Recommendations by Exposure Class](references/gwas_databases.md) <br>
- [IV Count Benchmarks and Weak-Instrument Risk by Exposure Class](references/iv_benchmarks.md) <br>
- [IEU Open GWAS](https://gwas.mrcieu.ac.uk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with optional R code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Always returns four workload configurations and one recommended primary plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
