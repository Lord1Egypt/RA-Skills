## Description:

Use the WordPress REST API for content operations only: auth setup (Application Password and Bearer), safe read/write flows for posts/pages/media, draft/publish/update patterns, taxonomy assignment, pagination/search, retry/rate-limit handling, and dry-run-first safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastiangansca](https://clawhub.ai/user/sebastiangansca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to safely read, create, update, publish, and manage WordPress posts, pages, media, categories, and tags through the WordPress REST API. It emphasizes dry-run-first writes, least-privilege authentication, dependency validation, and explicit approval before publishing or deleting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may target the wrong WordPress site or environment for a content write.

Mitigation: Confirm WP_SITE and staging or production context before writes, validate authentication with a read call, and perform a dry run first.

Risk: Publishing, deleting, or bulk-updating content could expose unintended changes.

Mitigation: Default changes to draft, require explicit approval for publishing or deleting, avoid destructive bulk updates unless specifically approved, and verify changed fields after each write.

Risk: Credentials or tokens used for WordPress API access could be over-privileged or exposed.

Mitigation: Use least-privilege WordPress accounts or scoped application passwords, avoid logging raw credentials, and rotate or revoke credentials after incidents or role changes.

## Reference(s):

- [Auth Setup](references/auth.md)
- [Safe Read/Write Flows](references/content-flows.md)
- [Taxonomy, Pagination, and Search](references/query-and-taxonomy.md)
- [Error, Retry, Rate-Limit, and Dry-Run Rules](references/reliability-and-safety.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance and example WordPress REST API requests; no generated files are required.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
