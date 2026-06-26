## Description: <br>
Generates Redis cache and data-structure commands from natural-language requests, covering String, Hash, List, Set, ZSet, Stream, queues, leaderboards, locks, and performance diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and backend engineers use this skill to draft Redis CLI and Python-client guidance for cache management, object storage, queues, leaderboards, distributed locks, and operational diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Redis commands can change or delete data or alter server configuration when run against a real instance. <br>
Mitigation: Review the Redis host, database, key pattern, and expected impact before execution, especially for delete, CONFIG, EVAL, and SLOWLOG RESET commands. <br>
Risk: Redis credentials or production connection details may be exposed if pasted into chat. <br>
Mitigation: Keep real Redis passwords out of prompts where possible and use environment variables or secret-management controls. <br>


## Reference(s): <br>
- [ClawHub Redis Skill Release](https://clawhub.ai/ryanlee-gemini/redis-skill) <br>
- [Redis Documentation](https://redis.io/docs/) <br>
- [Redis Commands](https://redis.io/commands/) <br>
- [Redis Latency and Performance Guidance](https://redis.io/topics/latency) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with Redis CLI and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may modify Redis data or server settings; review target host, database, key pattern, and impact before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
