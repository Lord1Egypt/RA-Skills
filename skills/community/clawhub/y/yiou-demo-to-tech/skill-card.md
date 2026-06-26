## Description: <br>
Converts business demos, product prototypes, and requirements into structured technical planning documents for engineering evaluation, task breakdown, scheduling, and acceptance review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiou](https://clawhub.ai/user/yiou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and project planners use this skill before development to turn demo material or business requirements into page flows, field and interface requirements, open questions, task breakdowns, acceptance criteria, and a maturity rating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business demos, prototypes, and requirements may contain confidential product details. <br>
Mitigation: Provide only material approved for the agent environment and avoid including sensitive internal data unless appropriate controls are in place. <br>
Risk: The skill may infer interfaces, data ownership, or business rules from incomplete demo material. <br>
Mitigation: Use its required source labels, open questions, and maturity blocking gaps to keep inferred items out of development entry until reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiou/yiou-demo-to-tech) <br>
- [Technical document template](artifact/templates/tech_doc_template.md) <br>
- [Structured output template](artifact/templates/structured_output_template.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown technical document plus structured JSON, open-question tables, task breakdowns, and acceptance criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires source labeling for key rules, interface assumptions, and data inferences; maturity ratings include blocking gaps when required inputs are missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
