## Description:

Use when a user asks to optimize, sharpen, clarify, rewrite, pressure-test, or improve an input, prompt, question, requirement, plan, idea, or message before sending it to an AI or person.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoyechen](https://clawhub.ai/user/gaoyechen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use SharpInput to turn vague, under-scoped, or high-stakes prompts, questions, plans, requirements, and messages into clearer copy-ready prompts while preserving the original intent. It is especially suited to prompt optimization workflows that need intent detection, scenario slots, context completion, pressure testing, and quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad agent, shell, and file permissions increase the impact of an unexpected or misrouted workflow.

Mitigation: Review the skill before installation and run it only in environments where those permissions are acceptable.

Risk: Bundled preference history may be read, updated, and reused across sessions without being obvious to the user.

Mitigation: Remove bundled preference files and disable or gate self-learning before normal use.

Risk: Subagent delegation can make prompt-improvement behavior harder to inspect during normal use.

Mitigation: Limit use to trusted workflows and review generated prompts before sending them to another AI or person.

## Reference(s):

- [SharpInput ClawHub Skill Page](https://clawhub.ai/gaoyechen/skills/sharpinput)
- [handoff-contract.md](references/handoff-contract.md)
- [intent-taxonomy.md](references/intent-taxonomy.md)
- [intent-details.md](references/intent-details.md)
- [interaction-patterns.md](references/interaction-patterns.md)
- [scenario-slot-templates.md](references/scenario-slot-templates.md)
- [prompt-patterns.md](references/prompt-patterns.md)
- [pressure-strategies.md](references/pressure-strategies.md)
- [output-templates.md](references/output-templates.md)
- [judge-rubric.md](references/judge-rubric.md)
- [self-learning.md](references/self-learning.md)
- [user-preferences.md](references/user-preferences.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured sections and a copy-ready prompt quote block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs identify the detected level, intent, scenario, context status, diagnosis, upgraded prompt, additions, trade-off note, and one minimal missing field when needed.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
