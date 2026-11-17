## Description:

Discord platform skill for SurfAgent, covering route-aware state checks, extraction-first workflows, blockers, and when to use the Discord adapter over raw browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surfagentapp](https://clawhub.ai/user/surfagentapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to navigate Discord through SurfAgent workflows, prioritizing route-aware checks, blocker detection, visible extraction, and verified actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide visible Discord state and message extraction in accounts, servers, or channels where access may be sensitive.

Mitigation: Use it only with accounts, servers, and channels where the operator has permission to view or act.

Risk: Discord login, verification, hCaptcha, or route mismatch states can block progress or make results misleading.

Mitigation: Require explicit blocker detection and report gated or wrong-surface states as real outcomes before continuing.

Risk: Discord's dynamic single-page interface can expose stale or shifted surfaces that make generic browser actions unreliable.

Mitigation: Prefer route-aware state checks and visible extraction, then verify the visible result after each action.

## Reference(s):

- [SurfAgent homepage](https://surfagent.app)
- [ClawHub skill page](https://clawhub.ai/surfagentapp/skills/surfagent-discord)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Text or Markdown guidance for browser and Discord-adapter workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; output depends on the active Discord task and visible browser state.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
