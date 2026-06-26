## Description: <br>
Semantic Cache helps agents cache LLM responses by meaning with Redis vector search so similar queries can reuse prior answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rylinjames](https://clawhub.ai/user/rylinjames) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add Redis-backed semantic caching around repeated LLM prompts, reducing repeated API calls and improving response time for similar questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cached prompts and responses may contain secrets, regulated data, or other sensitive content. <br>
Mitigation: Use a dedicated Redis database or namespace, avoid caching sensitive data unless policy permits it, and set an appropriate TTL. <br>
Risk: Clear and test commands remove cached Redis entries and the search index used by the skill. <br>
Mitigation: Run destructive commands only against a dedicated cache or test environment after confirming the target Redis connection. <br>
Risk: Semantic matches can return a cached answer for a similar but not identical query. <br>
Mitigation: Tune SEMANTIC_CACHE_THRESHOLD for the use case and review behavior before using cached responses in high-impact workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rylinjames/semantic-cache) <br>
- [OpenClaw homepage](https://github.com/openclaw/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses REDIS_URL and OPENAI_API_KEY; supports store, lookup, query, stats, clear, and test commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
