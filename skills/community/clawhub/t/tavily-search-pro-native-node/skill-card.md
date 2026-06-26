## Description: <br>
Research-grade Tavily toolkit for OpenClaw that supports web search, URL extraction, usage stats, response caching, JSONL usage logging, and rate-limit backoff through a native Node.js script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwestburg](https://clawhub.ai/user/jwestburg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill for deeper Tavily-backed web research, multi-URL content extraction, Tavily usage checks, cache inspection, and research workflows that need explicit freshness, logging, and credit controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and URLs are sent to Tavily using the user's API key. <br>
Mitigation: Use the skill only when external Tavily research is appropriate, and do not send sensitive or client/private research without explicit approval. <br>
Risk: Usage logs may retain plaintext queries or URLs, and cached results are stored locally. <br>
Mitigation: Use --no-log --no-cache for sensitive approved research, and periodically inspect or clear the cache and log directory. <br>
Risk: Cached results are not scoped to a Tavily API account when multiple accounts share the same OS profile. <br>
Mitigation: Use separate OS profiles or --no-cache when account separation matters. <br>
Risk: Advanced searches and extraction can consume Tavily credits and may hit rate limits. <br>
Mitigation: Prefer basic depth unless advanced research is justified, keep result counts focused, and use stats plus built-in retry/backoff behavior to monitor usage. <br>


## Reference(s): <br>
- [Tavily Search Pro Contract](artifact/references/tavily-pro-contract.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jwestburg/tavily-search-pro-native-node) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, human-readable command output, or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source URLs, cache and logging status, freshness and depth choices, limitations, caveats, and Tavily credit usage or estimates.] <br>

## Skill Version(s): <br>
1.0.11 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
