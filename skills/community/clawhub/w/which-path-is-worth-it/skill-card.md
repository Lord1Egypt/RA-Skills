## Description:

Helps an agent choose among two or more research or action paths under incomplete information by comparing success probability bounds, expected value, safe value, and optimistic value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to choose among competing research, implementation, or action paths when success rates, costs, and payoff estimates are uncertain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates computation and ledger-backed outcome lookup to the required clawphylax plugin.

Mitigation: Review the clawphylax plugin and its permissions before use, especially where ledger access is involved.

Risk: Recommendations depend on rough cost, value, and success assumptions that may not hold across attempts.

Mitigation: Check the estimates with the user, report probability bounds and decision-change conditions, and rerun after each attempt with updated counts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/which-path-is-worth-it)
- [Clawphylax homepage](https://github.com/aeneassoft/clawphylax)
- [ClawHub publisher profile](https://clawhub.ai/user/aeneassoft)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with an ACTION line, per-path metrics, and plan lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawphylax plugin for ledger-backed paths; manually supplied estimates can be used for explicit path comparisons.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
