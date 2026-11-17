## Description:

A Chinese-language dispatcher skill that evaluates user tasks and delegates work to five persistent sub-agents using fixed session keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjj2026](https://clawhub.ai/user/sjj2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run a Chinese-language multi-agent coordination workflow that triages tasks, assigns work to alpha/bravo/charlie/delta/echo sub-agents, monitors progress, and summarizes results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic delegation can route user work to multiple persistent sub-agents before the full scope is reviewed.

Mitigation: Use this skill only for workflows that need delegated multi-agent coordination, and review each task assessment before allowing dispatch.

Risk: Persistent alpha/bravo/charlie/delta/echo session reuse may carry context between tasks.

Mitigation: Reset or isolate sessions when switching projects or handling sensitive context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sjj2026/skills/shike-multi-agent)
- [Publisher Profile](https://clawhub.ai/user/sjj2026)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text task assessments, dispatch plans, progress reports, and final summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate multiple persistent sub-agent sessions with fixed alpha/bravo/charlie/delta/echo keys.]

## Skill Version(s):

1.5.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
