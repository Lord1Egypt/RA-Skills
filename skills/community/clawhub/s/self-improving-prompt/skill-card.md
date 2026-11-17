## Description:

Refines ambiguous or high-risk user requests before execution, while skipping clear single-step instructions and already well-scoped tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lq434239](https://clawhub.ai/user/lq434239)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide when a user request should be executed directly, silently refined, presented as a compare-first prompt, or returned as a refinement only. It helps clarify underspecified or high-risk work without adding friction to clear requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A refined prompt could unintentionally steer execution away from the user's original intent.

Mitigation: Use compare-first only when refinement adds substantial value or when the user asks to compare, and let the user choose between the refined and original prompt.

Risk: Prompt refinement can add unnecessary interruption for already clear requests.

Mitigation: Skip refinement for clear atomic instructions and prefer silent refinement when the user does not need to inspect the rewritten prompt.

Risk: Workflow preference learning could expose task details if full prompt text were stored.

Mitigation: Record only abstract preference labels and never store full refined prompt text or task-specific details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lq434239/skills/self-improving-prompt)
- [Decision Matrix](references/decision-matrix.md)
- [Reference Details](references/details.md)
- [Non-Examples](references/non-examples.md)
- [Prompt Refinement Patterns](references/prompt-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text with optional refined prompt blocks and concise user choice prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only behavior; no bundled scripts, external services, credentials, network access, or persistent configuration changes are required for normal use.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
