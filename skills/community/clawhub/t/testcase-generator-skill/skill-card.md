## Description: <br>
Generates functional test case documents in Excel-style format from requirements documents, API definitions, database schemas, and existing test case references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hughzmflying](https://clawhub.ai/user/hughzmflying) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and test teams use this skill to turn product requirements, OpenAPI or Swagger definitions, DDL scripts, and prior cases into structured functional, API, data, boundary, and priority-tagged test cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated test cases may miss requirements, misread API or schema details, or overstate coverage. <br>
Mitigation: Review generated cases manually against the source requirements, API definitions, database schemas, and existing regression suites before using them for release decisions. <br>
Risk: Input documents may contain sensitive product, database, or customer information. <br>
Mitigation: Process only files that are appropriate for the local execution environment and avoid supplying documents that the user is not authorized to process. <br>
Risk: The script depends on Python packages such as openpyxl. <br>
Mitigation: Install dependencies only from trusted package sources and run the script in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hughzmflying/testcase-generator-skill) <br>
- [Test case examples](references/testcase_examples.md) <br>
- [Priority guide](references/priority_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional Python CLI commands and generated Excel-style test case files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated cases should be treated as drafts and manually reviewed for coverage and correctness.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
