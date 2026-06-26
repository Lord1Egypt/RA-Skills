## Description: <br>
Designs complete, rigorous research plans for medicinal plant / TCM molecular mechanism studies against diseases (colorectal cancer, liver cancer, diabetes, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, biomedical analysts, and agent users use this skill to turn broad TCM or herbal medicine mechanism questions into structured, executable computational study plans. It focuses on network pharmacology, multi-omics integration, molecular docking, validation strategy, and clear separation between computational associations and causal experimental evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Biomedical research plans may be mistaken for clinical, dosing, regulatory, or patient-care advice. <br>
Mitigation: Use the skill only for computational research planning, keep the mandatory disclaimer, and redirect clinical, dosing, regulatory, or prescriptive requests to qualified professionals. <br>
Risk: Computational network pharmacology, immune deconvolution, and docking results can be overinterpreted as causal mechanism evidence. <br>
Mitigation: Require explicit language that computational findings suggest associations or hypotheses only, and reserve causal claims for experimental validation such as knockdown, rescue, in vivo, or organoid studies. <br>
Risk: Biomedical databases, target predictions, and thresholds can be incomplete, inconsistent, or unsuitable for a specific herb-disease pair. <br>
Mitigation: Independently verify biomedical sources and methods, document assumptions and thresholds, run sensitivity checks, and use fallback data sources when primary data are sparse. <br>


## Reference(s): <br>
- [Analytical Plan Steps](references/analytical_plan_steps.md) <br>
- [Critical Design Thinking](references/critical_design_thinking.md) <br>
- [Data Sources Reference](references/data_sources.md) <br>
- [Implementation Outline](references/implementation_outline.md) <br>
- [Milestones and Deliverables](references/milestones_deliverables.md) <br>
- [Minimal Executable Version](references/minimal_executable_version.md) <br>
- [Validation Strategy](references/validation_strategy.md) <br>
- [TCMSP](https://tcmsp-e.com) <br>
- [HERB](http://herb.ac.cn) <br>
- [Swiss Target Prediction](http://www.swisstargetprediction.ch) <br>
- [GeneCards](https://www.genecards.org) <br>
- [DisGeNET](https://www.disgenet.org) <br>
- [GEO](https://www.ncbi.nlm.nih.gov/geo) <br>
- [TCGA](https://portal.gdc.cancer.gov) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown research plan with tables, phased outlines, tool commands or code sketches when relevant, and a mandatory research-only disclaimer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should mark uncertain assumptions, avoid clinical or prescriptive claims, and distinguish computational association from causal validation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
