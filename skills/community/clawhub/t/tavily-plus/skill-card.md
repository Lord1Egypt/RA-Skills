## Description:

Enhanced Tavily search with multi-API key rotation, intent recognition, sub-question decomposition, summarization, and offline document export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fundou1081](https://clawhub.ai/user/fundou1081)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run Tavily-backed web searches with query routing, rate-limit failover across configured API keys, structured summaries, and optional markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and search queries may be sent to an untrusted endpoint if the Tavily base URL is changed.

Mitigation: Keep TAVILY_BASE_URL unset or pinned to the real Tavily API before use.

Risk: Sensitive search terms or source snippets may be retained in local markdown reports.

Mitigation: Avoid private internal material in queries and enable export_doc only when retaining the report on disk is acceptable.

Risk: The security verdict requires review before deployment.

Mitigation: Install only in trusted execution environments and review the configured Tavily endpoint and API key handling.

## Reference(s):

- [Tavily API](https://api.tavily.com)
- [ClawHub skill page](https://clawhub.ai/fundou1081/skills/tavily-plus)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON response with search intent, sub-questions, search results, summary text, metadata, and optional markdown report path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create timestamped markdown reports under the user's OpenClaw workspace when export_doc is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
