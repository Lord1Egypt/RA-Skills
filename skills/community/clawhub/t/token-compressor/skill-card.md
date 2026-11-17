## Description:

Pre-process prompts through three compression layers before sending to paid APIs, using a local Ollama model to compress messages and summarize conversation history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to reduce paid LLM API token usage by compressing long user messages, summarizing older conversation history, and checking an in-memory response cache before calling an external API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and conversation history may be sent to a configurable HTTP host while the documentation emphasizes localhost-only processing.

Mitigation: Configure ollamaHost only to a trusted loopback or local Ollama endpoint, and do not route sensitive or regulated data unless the local service and its logs are trusted.

Risk: Compressed messages and summaries can distort, omit, or inject context into later model calls.

Mitigation: Review compressed outputs in sensitive workflows, keep recent turns verbatim, and disable compression for messages where exact wording is required.

Risk: Cached responses are reused through keyword-based matching and may be stale or mismatched for a later request.

Mitigation: Use conservative cache size and TTL settings, reset the cache between unrelated conversations, and bypass caching for high-impact decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/token-compressor)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JavaScript API results and compressed conversation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Ollama service; compression may fall back to the original input, and cached responses are kept in memory only.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
