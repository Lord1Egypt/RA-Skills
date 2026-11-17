## Description:

Wraps an agent tool function with retry logic, result validation, exponential backoff, optional error repair, and optional idempotency-key caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayalili](https://clawhub.ai/user/ayalili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to make tool calls more tolerant of transient failures, invalid results, and repairable argument errors. It is best suited to idempotent or carefully controlled operations where repeated execution is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically repeat or modify high-impact tool calls while overstating its idempotency protection.

Mitigation: Use it only for idempotent or carefully controlled operations; avoid payments, writes, deletes, public posting, or database mutation unless the downstream system enforces real idempotency keys, scoped caching with expiry, and review of repaired commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayalili/skills/tool-call-retry)
- [Zod module used by the skill](https://deno.land/x/zod@v3.22.4/mod.ts)

## Skill Output:

**Output Type(s):** [API Calls, Code, Configuration]

**Output Format:** [Structured JavaScript object with success, data, attempts, fromCache, and error fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Executes the supplied tool function and may retry with modified arguments when an error handler returns repaired input.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
