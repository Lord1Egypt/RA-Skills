## Description:

Routes agent requests to cheap, default, pro, or ultra model tiers, with manual overrides, optional briefing for large context, feedback-based threshold adjustments, and response policy hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staratheris](https://clawhub.ai/user/staratheris)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to choose an appropriate model tier for each request, keep routine work on cheaper models, and escalate heavier work to stronger models or sub-agents with concise context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented shell invocation can be unsafe if an agent inserts raw user text into a shell command.

Mitigation: Call router.py with an argument-vector API or pass user text through stdin or another non-shell-interpolated channel.

Risk: The skill can auto-route work to stronger models or sub-agents and records local mode, feedback, and last-decision state.

Mitigation: Review routing rules before installation, confirm escalation behavior is acceptable, and monitor or reset the local state.json file when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/staratheris/skills/staratheris-arya-model-router)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands, Configuration]

**Output Format:** [JSON routing decisions and Markdown integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Router output includes level, model, score, reasons, actions, response policy, and helper script hints; briefing helper outputs compact text from stdin.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
