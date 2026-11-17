## Description:

Defines report-service SQL template variable, conditional block, loop, and result transformation rules for agents that generate reporting queries and response shaping steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[23396599](https://clawhub.ai/user/23396599)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to write report-service SQL templates with strict namespaced variables, optional SQL fragments, array loops, and post-query JSON transformations. It is intended for reporting workflows that need consistent query parameterization and response assembly patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe SQL substitution could occur if the report-service template engine does not safely escape or bind values in LIKE, IN, loop, or conditional fragment cases.

Mitigation: Before installation or use, confirm the skill is intended for the target report-service environment and verify the template engine safely escapes or binds all substituted SQL values.

Risk: Incorrect dynamic block boundaries can leave invalid SQL when optional variables are missing.

Mitigation: Keep logical operators and complete SQL fragments inside conditional blocks so omitted variables remove the full fragment cleanly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/23396599/skills/report-sql)
- [Transform reference](artifact/references/transform.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with SQL and JSON code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no hidden execution, persistence, or data-access behavior is reported in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
