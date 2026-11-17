## Description:

A/B evaluates AI agent skills through three-role isolation, generating skill profiles, synthetic test tasks, baseline versus with-skill comparisons, attribution analysis, and structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luarassassin](https://clawhub.ai/user/luarassassin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use SkillProbe to decide whether an AI agent skill is worth installing, compare skill versions, investigate performance changes, and produce evidence-backed evaluation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool-capable sub-agents may apply untrusted skill instructions while sensitive files, credentials, network tools, or write access are available.

Mitigation: Run evaluations only in a sandboxed or low-privilege agent environment with separate containment and logging before evaluating unknown skills.

Risk: Evaluation results can be invalid if skill content leaks into the baseline arm or the orchestrator executes test tasks itself.

Mitigation: Use separate baseline and with-skill sub-agent sessions, keep the baseline prompt free of skill content, and require dispatch evidence with distinct session IDs.

## Reference(s):

- [SkillProbe ClawHub release](https://clawhub.ai/luarassassin/skills/skillprobe)
- [Publisher profile](https://clawhub.ai/user/luarassassin)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown evaluation reports, JSON task-result arrays, prompt templates, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include weighted scores, attribution notes, recommendation labels, and dispatch evidence when the workflow is followed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
