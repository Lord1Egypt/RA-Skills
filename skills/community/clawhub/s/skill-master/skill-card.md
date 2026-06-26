## Description: <br>
Meta-skill for skill selection and routing. Use this skill FIRST when you are unsure which skill to use for a task. Provides a decision tree, keyword triggers, and guidance on combining multiple skills for complex workflows. Also use when onboarding to understand the full skill library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and agent operators use this skill to choose the appropriate skill for a user request, follow routing guidance, and understand the available skill library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires persistent logging of routing decisions, matched request phrases, and context. <br>
Mitigation: Use only where this logging is acceptable, or require optional analytics, redaction of user text, retention limits, deletion controls, and access documentation before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with tables, decision trees, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes to other skills and instructs agents to log each skill invocation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
