## Description: <br>
Consult the tool-models agent for model selection, cost estimation, capability queries, and provider comparisons when choosing models, comparing costs, checking availability, or answering which model to use for a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to query current model availability, capabilities, provider limits, cost estimates, and task-fit recommendations before selecting or configuring an AI model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model-selection prompts and workload estimates may include sensitive business context. <br>
Mitigation: Ask only for the model-selection details needed to answer the task, and remove unnecessary confidential customer, product, pricing, or volume details before querying the model advisor. <br>
Risk: Model prices, availability, context windows, and provider limits change over time. <br>
Mitigation: Query the model database or tool-models sub-agent at decision time instead of relying on static model knowledge. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seanford/skilled-models-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JavaScript and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are based on the queried model database rather than static model knowledge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
