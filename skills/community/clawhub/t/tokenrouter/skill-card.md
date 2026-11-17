## Description:

Token Router helps agents and developers choose cost-effective LLM tiers for tasks, model-routing workflows, and platform configuration while accounting for complexity, quality, and safety constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to select appropriate model tiers, estimate token cost tradeoffs, and produce routing or configuration guidance for multi-model agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to persist user preferences, session traces, and learning history without clear opt-in or retention limits.

Mitigation: Configure preference learning, session traces, and monthly reports as opt-in, minimize retained data, and provide a clear deletion path.

Risk: Model pricing and provider capabilities can change after a recommendation is generated.

Mitigation: Verify current provider or OpenRouter pricing before acting on cost-sensitive routing decisions.

## Reference(s):

- [Source repository](https://github.com/qomob/TokenRouter)
- [OpenRouter](https://openrouter.ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with concise recommendations, estimates, routing summaries, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model tiers, estimated token costs, safety upgrades, and optional routing reports.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
