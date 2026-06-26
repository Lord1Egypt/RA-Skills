## Description: <br>
Provides an external entry point to a software development cost-estimation dashboard for project budgeting, scoping, and quote planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business, product, and technical stakeholders use this skill when they need to estimate software development costs, align budgets, or prepare quote discussions. The skill returns an external dashboard entry point where the assessment workflow continues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct project plans, pricing, customer details, staffing assumptions, architecture notes, credentials, or regulated business information to a third-party site. <br>
Mitigation: Install and use it only when the external cost-estimation dashboard is intended, and review the destination site's operator, privacy terms, retention practices, and approval requirements before entering sensitive information. <br>
Risk: Server security review marked the release suspicious because disclosure and user-control safeguards for the external destination may be insufficient. <br>
Mitigation: Treat the external-link handoff as a review point before deployment and require user confirmation before sharing sensitive project or budget data. <br>


## Reference(s): <br>
- [Software Cost Dashboard](https://soft.ai-skills.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/allinherog-star/software-dev-cost-dashboard) <br>
- [Skill configuration reference](references/skill.json) <br>
- [Form schema reference](references/form-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [JSON response containing an external web application URL, label, invocation mode, and message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [External-link mode; assessment inputs and outputs are handled on the destination site.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
