## Description:

When unsure which thinking skill fits, map domain and problem type, then return NONE or one primary skill by default (at most three complementary).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to choose whether to invoke a thinking framework, select one primary thinking skill by mechanism fit, or return NONE when no framework clearly helps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill influences how an agent chooses among thinking frameworks, which can lead to unnecessary or misleading routing if used when the fit is already obvious or no framework would help.

Mitigation: Use the skill's short-circuit and over-application guards: return NONE when no route clearly improves the work, choose one primary route by default, and allow multi-skill routing only for distinct complementary roles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-model-router)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Structured text routing recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns NONE, one route, or up to three routes with roles, unique questions, rationale, blind spots, and exit criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
