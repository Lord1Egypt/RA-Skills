## Description:

Coordinates multi-skill task routing, context handoff, critic review, conflict arbitration, retry handling, fallback handling, and final structured output for complex agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route complex tasks across downstream skills with executor and critic review, context-preserving handoffs, arbitration, retries, and fallback closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad task-routing authority could forward sensitive session context to unrelated downstream skills.

Mitigation: Use the skill only in hosts that enforce higher-priority instructions and per-skill data minimization; keep the data envelope limited to task-relevant fields.

Risk: Centralized routing and final-format control could conflict with user-requested output formats or host policy.

Mitigation: Require the host to enforce user-requested formats and higher-priority policy before accepting the orchestrator's final response.

Risk: Fallback or arbitration decisions could introduce incorrect or misleading guidance if accepted without review.

Mitigation: Review the decision, critic insight, and arbitration result before acting on downstream recommendations, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/smallkeyboy-task-orchestrator)
- [ClawHub publisher profile](https://clawhub.ai/user/smallkeyboy)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON response containing stage, status, decision, critic insight, arbitration, next action, data envelope, and retry count.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves required orchestration fields even when a field is temporarily not applicable.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
