## Description:

Search UniProfit trade intelligence data through the OpenClaw-compatible UniProfit API when Codex or OpenClaw needs importer lookup, exhibition lead search, or purchase requirement search with a user-created trade_search API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieziqing](https://clawhub.ai/user/xieziqing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to query UniProfit-owned importer, exhibition lead, and procurement requirement datasets with a configured trade_search API key. It helps plan structured searches, execute supported UniProfit API queries, and summarize actionable trade leads without dumping raw payloads by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts can send the API key and search queries to a non-HTTPS or misconfigured API base URL.

Mitigation: Use a fixed, trusted HTTPS UniProfit API base URL and rotate the API key if it may have been used with HTTP.

Risk: Trade searches may consume paid quota or expose commercially sensitive search filters to the configured UniProfit service.

Mitigation: Validate the credential and query plan before execution, and treat search filters and returned leads as commercially sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xieziqing/skills/uniprofit-trade-search)
- [API Reference](references/api.md)
- [Query Patterns](references/query-patterns.md)
- [Error Handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional shell command examples and structured search details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries describe the current result window, filters used, whether more results may exist, and suggested query refinements.]

## Skill Version(s):

1.0.6 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
