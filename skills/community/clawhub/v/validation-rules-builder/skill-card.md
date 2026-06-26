## Description: <br>
Build validation rules for construction data. Create RegEx and logic-based validation for BIM elements, cost codes, and schedule data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction project managers, BIM coordinators, cost managers, schedulers, and developers use this skill to define and apply validation rules for construction records, including WBS codes, cost codes, schedule activities, and BIM element metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read or export local project data during validation workflows. <br>
Mitigation: Keep input and export paths explicit, and review generated validation outputs before sharing them. <br>
Risk: Custom validation functions or generated rules may misclassify project records. <br>
Mitigation: Review custom logic before execution and validate rule behavior against representative construction data. <br>
Risk: Cost estimates or cost analysis outputs may be incomplete or unsuitable for financial decisions. <br>
Mitigation: Treat cost-related outputs as advisory and confirm them against authoritative project and financial sources. <br>


## Reference(s): <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/validation-rules-builder) <br>
- [Publisher profile](https://clawhub.ai/user/datadrivenconstruction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with structured tables and optional Python code examples, CSV, Excel, or JSON export guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize validation results with issue counts, affected fields, severity, and suggested fixes.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact/claw.json lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
