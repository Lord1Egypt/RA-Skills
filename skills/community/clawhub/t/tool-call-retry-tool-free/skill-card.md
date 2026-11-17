## Description: <br>
A free tool-call retry skill for personal developers that wraps LLM or API tool calls with exponential backoff, result validation, and optional idempotency keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to make LLM and external API tool calls more resilient by adding retry behavior, result validation, and idempotency guidance. It is intended for personal-development workflows that need lightweight reliability improvements around asynchronous tool functions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retries of write-capable actions such as payments, deletes, saves, or exports can duplicate side effects. <br>
Mitigation: Use the skill primarily for read-only or clearly idempotent calls, and require idempotency keys, deduplication, user confirmation, and explicit retry exclusions for state-changing operations. <br>
Risk: Broad retry behavior can amplify downstream load or repeat non-recoverable failures. <br>
Mitigation: Keep retry counts bounded, use exponential backoff, validate results carefully, and avoid retrying authorization, validation, or other non-recoverable errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tool-call-retry-tool-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples and JSON-shaped response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes retry parameters such as toolFn, args, maxRetries, initialDelayMs, validatorFn, and idempotencyKey.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
