## Description: <br>
根据项目属性（如Competency、名称、描述、EP、公司类型等），从预定义的解决方案列表中为其标注最合适的Solution标签。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luorixin](https://clawhub.ai/user/luorixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and project teams use this skill to classify project records into the most appropriate Solution label using required project fields, competency mappings, matching rules, and validation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project records may contain sensitive project descriptions, company types, or partner names. <br>
Mitigation: Confirm the provided records are appropriate to process in the agent environment before using the skill. <br>
Risk: Classification may be incorrect when a record lacks required fields or only matches broad semantic rules. <br>
Mitigation: Review low-confidence, validation-failed, downgraded, or unclassified outputs before using them in reporting or operational workflows. <br>


## Reference(s): <br>
- [Competency Solution Mapping CSV](artifact/assets/Competency的Solution清单.csv) <br>
- [ClawHub Skill Page](https://clawhub.ai/luorixin/solution-tag) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table or structured records with matched Solution labels, confidence, validation status, and processing notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adds Matched_Solution, Match_Confidence, Validation_Status, and Processing_Notes fields to each project record.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
