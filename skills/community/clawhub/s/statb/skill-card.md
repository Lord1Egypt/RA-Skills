## Description:

Pushes real-time numeric progress and task metrics to a live statb.io dashboard during long-running agent work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianlong2005](https://clawhub.ai/user/qianlong2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to expose progress counters, rates, status, timing, and other numeric metrics for long-running or multi-step tasks on a browser-based statb.io board.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send progress metrics to a public third-party dashboard before the user has explicitly opted in.

Mitigation: Require explicit confirmation before use, disclose the statb.io board URL, and make progress publishing optional for the task.

Risk: Board IDs, metric names, or metric values could reveal sensitive project, customer, infrastructure, model, or deployment information.

Mitigation: Use sanitized board IDs and metric keys, send only numeric progress metrics, and avoid filenames, secrets, PII, infrastructure labels, and sensitive model or deployment metrics.

Risk: Generated scripts may embed statb.io curl calls or timers that continue sending updates longer than intended.

Mitigation: Review generated scripts before execution, keep push calls scoped to meaningful task stages, and ensure finalization disables recurring updates.

## Reference(s):

- [statb.io](https://statb.io)
- [ClawHub skill page](https://clawhub.ai/qianlong2005/skills/statb)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with bash curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces numeric statb.io push updates; the free tier supports up to 16 metrics per board.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
