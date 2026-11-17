## Description:

Build and debug Querit.ai integrations for /v1/search web results and /v1/contents page extraction using API-key authenticated JSON requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinkybb](https://clawhub.ai/user/vinkybb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, review, and troubleshoot Querit.ai search and page-content integrations in applications, RAG pipelines, and agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected search queries or URLs to Querit's API when used for live integration testing.

Mitigation: Use it only for intended Querit.ai integrations and avoid sending sensitive queries or URLs unless the deployment is approved for that data.

Risk: QUERIT_API_KEY is required for live calls and could be exposed through logs or committed configuration.

Mitigation: Store the key as a secret or environment variable, never hardcode it, and redact Authorization headers from logs.

Risk: Using the documented Python SDK in production without review can introduce dependency drift.

Mitigation: Pin and review the querit SDK version before production use.

Risk: Plan limits, endpoint entitlements, rate limits, and partial crawl results can produce incomplete or failed retrievals.

Mitigation: Run the smoke test first, throttle requests to the account QPS, check per-URL statuses, and handle missing page text explicitly.

## Reference(s):

- [Querit homepage](https://www.querit.ai)
- [Querit official docs](https://www.querit.ai/en/docs/overview/about)
- [POST /v1/search](references/search-api.md)
- [POST /v1/contents](references/contents-api.md)
- [Python integration](references/python-integration.md)
- [Failure modes](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/vinkybb/skills/querit-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request payloads, integration snippets, troubleshooting steps, and smoke-test commands; live calls require QUERIT_API_KEY.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
