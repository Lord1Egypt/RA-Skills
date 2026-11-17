## Description:

X platform skill for SurfAgent, covering route-aware workflows, proof rules, blockers, and when to use the X adapter over raw browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surfagentapp](https://clawhub.ai/user/surfagentapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use SurfAgent X to operate X/Twitter workflows with route-aware checks, account verification, posting and reply safeguards, engagement verification, and recovery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through public X actions such as posts, replies, follows, reposts, likes, and community joins.

Mitigation: Use it only with accounts the agent is intended to control, and review user-facing actions when their content or audience matters.

Risk: X UI state can be ambiguous, delayed, or tied to the wrong logged-in account.

Mitigation: Verify the active account, route, target surface, and visible post-action result before treating an action as complete.

Risk: Composer text may appear visually present while X has not accepted it as real input.

Mitigation: Inspect composer state and use real keyboard-style input recovery before submitting when the Post or Reply button remains disabled.

## Reference(s):

- [SurfAgent homepage](https://surfagent.app)
- [ClawHub SurfAgent X listing](https://clawhub.ai/surfagentapp/skills/surfagent-x)
- [X State Map](artifact/X_STATE_MAP.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance for agent workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes visible verification before claiming X account actions succeeded.]

## Skill Version(s):

1.2.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
