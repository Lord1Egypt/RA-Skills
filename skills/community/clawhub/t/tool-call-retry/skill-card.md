## Description: <br>
Retries and validates agent tool calls with exponential backoff, optional error correction, and idempotency support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ayalili](https://clawhub.ai/user/Ayalili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to wrap asynchronous tool functions that may fail or return malformed data. It helps retry calls, validate results, repair arguments through a custom handler, and use idempotency keys for repeat-safe workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blind retries can repeat side-effecting actions such as spending money, modifying data, sending messages, or deleting content. <br>
Mitigation: Require explicit user approval for side-effecting calls, use idempotency keys or deduplication, and apply least-privilege credentials. <br>
Risk: Automatic error correction can change tool arguments before a retry. <br>
Mitigation: Constrain error handlers and require human review before executing repaired arguments for sensitive operations. <br>
Risk: Cached idempotent results may retain sensitive data within the runtime boundary. <br>
Mitigation: Avoid caching sensitive results unless the runtime environment is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ayalili/tool-call-retry) <br>
- [Zod v3.22.4 module](https://deno.land/x/zod@v3.22.4/mod.ts) <br>


## Skill Output: <br>
**Output Type(s):** [JSON] <br>
**Output Format:** [Structured object with success, data, attempts, fromCache, and error fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Retries are bounded by maxRetries with exponential backoff; optional idempotency keys can return cached results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
