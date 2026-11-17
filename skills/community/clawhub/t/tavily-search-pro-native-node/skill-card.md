## Description:

Research-grade Tavily web search for OpenClaw using native Node.js with zero dependencies, supporting deep web research, multi-URL extraction, estimated credit tracking, response caching, usage-log review, and 429 backoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwestburg](https://clawhub.ai/user/jwestburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research agents use this skill to run Tavily-backed web searches, extract content from public URLs, inspect usage statistics, and manage response cache behavior while tracking estimated credit use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and accepted public URLs are sent to Tavily with the configured API key.

Mitigation: Use this skill only for queries and URLs approved for external Tavily processing, and classify privacy sensitivity before outbound search or extract use.

Risk: Usage logs may contain plaintext queries or URLs, and cached responses may persist under the skill-specific OpenClaw cache directory.

Mitigation: Use --no-log --no-cache for sensitive or client/private research that is approved for external processing.

Risk: Cached responses are not scoped by Tavily account when multiple accounts share one OS profile.

Mitigation: Use separate OS profiles for account isolation or disable caching with --no-cache.

Risk: The cache clear subcommand deletes local cached response files.

Mitigation: Run cache clear only when deletion is intentional; the skill limits deletion to expected cache files under its own cache directory and reports partial failures.

## Reference(s):

- [Tavily Search Pro Contract](references/tavily-pro-contract.md)
- [ClawHub Skill Page](https://clawhub.ai/jwestburg/skills/tavily-search-pro-native-node)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON command output with source URLs, cache/logging status, freshness and depth choices, estimated credit use, caveats, and next-step guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit raw JSON when requested; normal usage returns compact human-facing text.]

## Skill Version(s):

1.0.36 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
