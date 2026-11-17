## Description:

Autonomous decision engine for AI agents with multi-objective optimization, risk assessment, decision trees, and reinforcement learning capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local decision-model utilities for ranking options, scoring risks, building decision trees, and experimenting with Q-learning behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented DecisionEngine facade is not exported by src/index.js, which may cause integration failures for users following the README-style usage example.

Mitigation: Import and test the exported classes directly, or add and verify a DecisionEngine facade before relying on the documented API.

Risk: The reinforcement learner reset path sets epsilon back to a fixed value, which can override a caller's custom exploration setting.

Mitigation: Check epsilon after reset in workflows that tune exploration, and restore the desired value before continuing training.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-agent-decision-engine)
- [Publisher profile](https://clawhub.ai/user/yuyonghao-123)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [JavaScript modules and Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local execution with no network, persistence, or hidden data-access behavior reported by security evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
