## Description: <br>
Generates structured Excel test cases from Markdown, PDF, Word requirement documents, or image flowcharts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
QA engineers, developers, and product teams use this skill to turn requirements, API documentation, design documents, and process diagrams into traceable manual test cases and formatted Excel reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow reads and transforms local requirement documents that may contain confidential product or customer information. <br>
Mitigation: Use only intended input files, keep outputs in an approved location, and avoid processing confidential requirements unless the workspace is approved for that data. <br>
Risk: Generated JSON and Excel test cases may omit requirements, misclassify priority, or include incorrect expected results. <br>
Mitigation: Review the staged JSON and formatted Excel output against the source requirements before relying on the generated test cases. <br>
Risk: The skill writes local output files, including staged JSON and Excel workbooks. <br>
Mitigation: Confirm the output directory before running the workflow and inspect generated files before sharing or importing them into QA systems. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/kokxi/skills/qa-testcase-generator) <br>
- [README](README.md) <br>
- [Test Design Methods](references/design_methods.md) <br>
- [Quality Checklist and Generation Rules](references/quality.md) <br>
- [Image and Flowchart Analysis](references/image_analysis.md) <br>
- [Test Case Templates](references/templates.md) <br>
- [Evaluation Schema](references/schemas.md) <br>
- [Runtime Environment](references/environment.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Benchmark Report](docs/iteration2-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with structured JSON intermediates and formatted Excel file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged JSON artifacts for traceability and an Excel workbook with priority coloring and business-domain separator rows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
