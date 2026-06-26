## Description: <br>
Generate a 4-sheet Excel review summary from Guanglianda export data for budget review projects, with automatic classification of review line items into seven standard adjustment categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lialia691691-alt](https://clawhub.ai/user/lialia691691-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Budget review practitioners and developer-assistant users use this skill to turn Guanglianda review export folders into a structured Excel review package. It is intended for workflows that need review drafts, summary tables, source-row mappings, and categorized adjustment detail sheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated review-line classification can misclassify items whose reasons are implicit, mixed, or outside the keyword rules. <br>
Mitigation: Review the generated category mappings, especially material-price, quota-subitem, base-adjustment, and high-value other entries, before relying on the workbook. <br>
Risk: The skill processes local Excel exports and produces a workbook that may influence budget review decisions. <br>
Mitigation: Use intended project data only, review commands before execution, and validate generated totals and classifications against the source exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lialia691691-alt/review-summary) <br>
- [Classification rules](references/classification.md) <br>
- [Template structure](references/template_structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Excel workbook plus concise command and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a four-sheet .xlsx review package covering review draft, summary, source-row mapping, and adjustment details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
