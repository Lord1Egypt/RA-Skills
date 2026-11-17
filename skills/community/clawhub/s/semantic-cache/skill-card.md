## Description:

Semantic Cache helps agents cache LLM API responses by semantic similarity using Redis vector search, OpenAI embeddings, and a configurable similarity threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rylinjames](https://clawhub.ai/user/rylinjames)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to reduce repeated LLM calls by checking a Redis semantic cache before making an API request and storing responses for similar future queries. It is suited to repetitive question-answering workflows such as support bots, FAQ agents, and internal assistants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared Redis cache can expose or overwrite cached prompts and responses across users or tenants.

Mitigation: Use a dedicated Redis database or isolated namespace, and restrict use to non-sensitive prompts unless tenant-aware access controls are added.

Risk: The clear command and stress test can delete broad cache data when pointed at shared or production Redis.

Mitigation: Run destructive commands only against disposable or dedicated Redis instances, never against shared or production databases.

Risk: Dependency behavior and security posture can change after installation.

Mitigation: Review dependency updates before installation and maintain normal package scanning in the deployment pipeline.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rylinjames/skills/semantic-cache)
- [OpenClaw ClawHub homepage](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JavaScript-based CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses REDIS_URL, OPENAI_API_KEY, SEMANTIC_CACHE_THRESHOLD, and SEMANTIC_CACHE_TTL; produces cache hit, miss, stats, clear, and query behavior for agent workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
