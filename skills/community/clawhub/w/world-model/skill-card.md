## Description:

World Model - Environment understanding, causal reasoning, and prediction for AGI

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobisamaa](https://clawhub.ai/user/tobisamaa)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to track environment state, reason over causal relationships, predict action outcomes, run what-if analysis, and assess risks before agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist broad local telemetry about the agent, user intent, environment, tools, sessions, actions, predictions, and business context.

Mitigation: Use it in a private workspace, review or delete JSON state and prediction log files regularly, and avoid including secrets or sensitive user content in prediction contexts until retention and redaction controls are added.

Risk: Local state and prediction logs can become stale or misleading if they are treated as authoritative environment truth.

Mitigation: Review generated predictions and risk assessments before acting, and refresh or reset stored state when the runtime context changes materially.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobisamaa/skills/world-model)
- [ClawHub publisher profile](https://clawhub.ai/user/tobisamaa)
- [Pearl, Causality: Models, Reasoning, and Inference](artifact/SKILL.md)
- [Ha and Schmidhuber, World Models](artifact/SKILL.md)
- [Artifact causal model](artifact/causal-model.json)
- [Artifact world state schema and sample state](artifact/world-state.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-shaped state, prediction, and causal model examples plus PowerShell-style API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write local JSON state and prediction log files when integrated with an agent runtime.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
