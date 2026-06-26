## Description: <br>
Assess translational gaps between preclinical models and human diseases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, translational scientists, and developers use this skill to generate structured reports that compare preclinical model limitations against a target human disease and identify clinical translation risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated gap scores and recommendations could be mistaken for medical, regulatory, or clinical advice. <br>
Mitigation: Treat outputs as research support and require qualified human review before using them for clinical, regulatory, or trial-design decisions. <br>
Risk: The optional output path can write files in the local workspace. <br>
Mitigation: Use explicit workspace output paths, avoid important existing files, and review generated files before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/translational-gap-analyzer) <br>
- [Audit Reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown, JSON, or table-formatted translational-gap reports with CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include gap scores, risk levels, dimension-level concerns, clinical failure predictors, recommendations, and assumptions or unresolved inputs when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
