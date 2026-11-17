## Description:

每次AI回复后自动分析本轮实际调用的专项技能，在回复末尾追加汇报。自动挂载，无需命令触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chn012cjus](https://clawhub.ai/user/chn012cjus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to append a concise record of specialized skills used in the current agent turn. It is intended for visibility into skill usage, not for exact audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill globally alters every assistant reply, which can disrupt workflows that require exact JSON, code-only output, or stable response formatting.

Mitigation: Install only where an always-on Chinese skill-usage footer is desired, and avoid using it for strict machine-readable or code-only outputs unless the behavior is made opt-in.

Risk: The bundled reporting script writes skill usage records to a local temporary log path, which may be unsuitable for privacy-sensitive or reliable audit workflows.

Mitigation: Review the logging behavior before deployment and revise it to use a private per-user location, retention controls, or no logging for sensitive workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chn012cjus/skills/skill-steward)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown footer text appended to agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce a local plain-text usage report when the bundled reporting script is run.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
