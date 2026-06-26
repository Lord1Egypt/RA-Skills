## Description: <br>
Monitor Redis server health, memory, performance, and BullMQ queues. Check queue depths, inspect failed jobs, analyze slow queries, and diagnose issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musaraf-m](https://clawhub.ai/user/musaraf-m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Redis health, memory, client activity, slow queries, and BullMQ queue state. It helps diagnose production Redis and BullMQ issues through read-only checks and concise remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redis credentials or connection details may be exposed through REDIS_URL or diagnostic output. <br>
Mitigation: Use a read-only or least-privilege Redis account, verify REDIS_URL targets the intended server, avoid putting passwords directly on command lines, and keep credential masking enabled. <br>
Risk: Diagnostics may contain sensitive operational data such as slow logs, BullMQ job payloads, stack traces, keys, and connection details. <br>
Mitigation: Redact slow logs, job payloads, stack traces, keys, and connection details before sharing output outside the trusted operations context. <br>
Risk: Running destructive Redis commands against a production instance could modify or delete data. <br>
Mitigation: Keep usage read-only and avoid destructive or mutating commands such as FLUSHDB, FLUSHALL, DEL, UNLINK, SET, EXPIRE, and CONFIG SET. <br>


## Reference(s): <br>
- [Redis Commands Quick Reference](references/redis-commands.md) <br>
- [Sentinal Redis ClawHub Listing](https://clawhub.ai/musaraf-m/sentinal-redis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline Redis CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Redis diagnostics; may include health summaries, queue counts, warning messages, and redaction guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
