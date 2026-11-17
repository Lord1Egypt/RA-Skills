## Description:

Closed-loop learning for AI coding agents that captures errors and corrections, recalls relevant past solutions, and promotes recurring patterns to project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharoonsharif](https://clawhub.ai/user/sharoonsharif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use Reflexion to preserve lessons from command errors, user corrections, and non-obvious fixes so similar future tasks can recall known resolutions and promote recurring project rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores coding-session data in local .reflexion entries.

Mitigation: Use it only in trusted projects, keep .reflexion out of sensitive repositories, and do not commit .reflexion data unless the contents have been reviewed.

Risk: Recall and promotion can inject stored learnings into future agent context or CLAUDE.md.

Mitigation: Disable or gate automatic recall and promotion until the security guidance is addressed, and review promoted rules before relying on them.

Risk: The authoritative security verdict is suspicious because shell-hook behavior and implementation details require review before use.

Mitigation: Review the shell scripts before installation and avoid global hooks until raw entry injection, promotion behavior, eval usage, and path interpolation are fixed.

## Reference(s):

- [Integration Guide](artifact/references/integration.md)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, XML-like recall blocks, JSON entries, and shell hook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local .reflexion entries and may append learned rules to CLAUDE.md when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
