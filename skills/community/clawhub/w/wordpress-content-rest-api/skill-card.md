## Description: <br>
Interact safely with WordPress content via REST API for posts, pages, media, taxonomies, supporting drafts, updates, pagination, search, and retry handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastiangansca](https://clawhub.ai/user/sebastiangansca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and content teams use this skill to inspect, draft, update, publish, and manage WordPress posts, pages, media, categories, and tags through the REST API while following dry-run-first and least-privilege workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure or over-broad WordPress permissions could grant unintended content access. <br>
Mitigation: Use HTTPS, least-privilege application passwords or scoped bearer tokens, avoid logging raw credentials, and rotate or revoke credentials after incidents or role changes. <br>
Risk: Writes to the wrong environment or premature publishing can alter live WordPress content. <br>
Mitigation: Verify the base URL and staging versus production target, run a dry run, read before writing, default writes to draft, and require explicit approval for publishing, deletion, media uploads, taxonomy creation, or bulk updates. <br>
Risk: Bulk or repeated REST API operations can hit rate limits or leave partial updates. <br>
Mitigation: Use bounded retries with backoff for retryable failures, keep request bursts small, serialize writes when content integrity matters, and halt on unexpected failures before continuing. <br>


## Reference(s): <br>
- [Auth Setup](references/auth.md) <br>
- [Safe Read/Write Flows](references/content-flows.md) <br>
- [Taxonomy, Pagination, and Search](references/query-and-taxonomy.md) <br>
- [Error, Retry, Rate-Limit, and Dry-Run Rules](references/reliability-and-safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with REST API request examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sanitized API response summaries, dry-run change plans, and verification steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
