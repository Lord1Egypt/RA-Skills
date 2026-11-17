## Description:

Auto-route tasks to the cheapest z.ai (GLM) model that works correctly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[princnl](https://clawhub.ai/user/princnl)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to classify tasks by complexity and choose an appropriate z.ai (GLM) model tier before responding. It is intended to reduce model spend while escalating work that needs stronger reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subjective routing rules may select a cheaper model for work that needs stronger reasoning.

Mitigation: Configure Standard or Plus/32B as the default for sensitive, safety-critical, legal, financial, security, or production-impacting tasks.

Risk: Cost-saving defaults can under-prioritize correctness for complex or ambiguous requests.

Mitigation: Escalate when a task requires more than brief focused thinking, involves architecture or critical decisions, or when Standard struggles with complexity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/princnl/skills/smart-model-routing-for-zai)
- [Skill Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with model-selection rules, examples, command snippets, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory routing decisions and examples; it does not execute code.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
