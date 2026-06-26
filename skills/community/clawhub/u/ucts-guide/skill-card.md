## Description: <br>
Smart task analysis with optimal tool prescription for coding tasks by complexity, domain, scope, and risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muthukumaran-k-1](https://clawhub.ai/user/muthukumaran-k-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to classify coding work and choose an appropriate UCTS-guided workflow, including risk overrides for security-sensitive, destructive, or high-complexity tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for more coding requests than intended and steer unrelated or sensitive work. <br>
Mitigation: Keep activation scoped to coding workflow triage, and disable or narrow the skill if it starts guiding unrelated tasks. <br>
Risk: Workflow recommendations can include risk-sensitive actions such as careful handling of security, payment, OAuth, or destructive-code tasks. <br>
Mitigation: Follow the skill's risk overrides for high and critical risk work, including disabling compression for critical tasks and adding careful review for high-risk changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline command examples and workflow recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task classification, recommended tool combinations, estimated savings, and dispatch instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
