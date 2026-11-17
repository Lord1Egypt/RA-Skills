## Description:

Token and context window optimization -- compact prompts, reduce redundancy, prioritize critical context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nakedoshadow](https://clawhub.ai/user/nakedoshadow)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to keep long coding and research sessions within useful context limits by reading narrower evidence, compacting completed work, and producing concise responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Over-compression or narrow file reads may omit details needed for accuracy.

Mitigation: Preserve active objectives, important decisions, errors, and directly relevant evidence when compacting context.

Risk: Terser responses may leave users without enough rationale for consequential changes.

Mitigation: Use concise prose while still stating assumptions, risks, and verification results for material decisions.

Risk: Subagent delegation can separate exploration from implementation context.

Mitigation: Require returned findings to include the specific files, lines, and conclusions needed for the main agent to act.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nakedoshadow/skills/shadows-context-optimizer)
- [Publisher homepage](https://clawhub.ai/NakedoShadow)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Inline agent behavior guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files, commands, network calls, or separate reports are produced by the skill.]

## Skill Version(s):

1.1.0 (source: release evidence and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
