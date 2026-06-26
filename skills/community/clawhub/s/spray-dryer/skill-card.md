## Description: <br>
Spray Dryer guides agents through generating spray dryer CAD drawings on JixieTools by selecting a product, collecting parameters, calculating values, creating a guest production sheet, and polling for output files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realsanyu](https://clawhub.ai/user/realsanyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and engineering assistants use this skill to walk through a Chinese-language spray dryer CAD generation workflow, including product selection, parameter collection, calculation review, production sheet creation, and progress monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a concrete product/category mismatch that could send users into the wrong CAD generation workflow. <br>
Mitigation: Verify that the listed category and product IDs match the intended spray dryer workflow on jixietools.com before using generated CAD artifacts or production sheets. <br>
Risk: The workflow can generate production sheets and CAD outputs through unauthenticated guest endpoints. <br>
Mitigation: Review selected products, parameters, calculated values, and output files before relying on them for engineering, purchasing, or fabrication decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/realsanyu/spray-dryer) <br>
- [realsanyu publisher profile](https://clawhub.ai/user/realsanyu) <br>
- [JixieTools API base](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Chinese Markdown with curl command examples, parameter tables, status updates, and generated production-sheet links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are interactive and stepwise; the agent waits for user confirmation before proceeding between major workflow steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
