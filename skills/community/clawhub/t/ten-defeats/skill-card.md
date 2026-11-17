## Description:

Use when Codex is asked to plan, design, implement, modify, refactor, debug, test, review, verify, or complete non-trivial software work; use Computer Use or operate a browser, desktop UI, or live app; coordinate multiple tools; or delegate to agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yofine](https://clawhub.ai/user/yofine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep non-trivial Codex software work grounded in clear intent, causal diagnosis, evidence-based validation, and honest completion claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Because this is an intentionally broad workflow guardrail, it may influence many non-trivial coding sessions automatically.

Mitigation: Install it only when stricter planning, evidence, and verification discipline is desired for the agent's normal software-work behavior.

Risk: The skill can encourage the agent to ask for clarification when missing choices are consequential and cannot be discovered safely.

Mitigation: Treat those clarification points as decision gates for user authority, not as failures to proceed.

Risk: The skill guards completion claims, so it may report work as partial when direct acceptance evidence is unavailable.

Mitigation: Provide access to the real runtime, source of truth, or acceptance path needed to verify the requested outcome.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Natural-language guidance, Markdown responses, code edits, shell commands, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Broadly applicable workflow guardrail; no code execution, data access, or hidden behavior found in security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
