## Description:

When one mental model leaves a material blind spot on a multi-domain or high-stakes problem, sequence complementary models with named roles and a conflict rule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to decide when multiple complementary reasoning models are justified, assign each model a distinct role, resolve conflicts with a predeclared rule, and synthesize one recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence how an agent structures complex decisions, and an over-applied or poorly separated model combination could produce misleading guidance.

Mitigation: Use the skill only when a named blind spot remains, require each model to answer a distinct question, predeclare the conflict rule, cap the combination at three models, and stop when a single model suffices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-model-combination)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Structured Markdown or text decision synthesis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution or system access; the workflow caps combinations at three models and requires distinct roles, a conflict rule, and a stop reason.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
