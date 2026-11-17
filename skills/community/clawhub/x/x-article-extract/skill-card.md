## Description:

Extracts full content from X/Twitter posts, X Articles, and external pages shared through t.co links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuxiaoyang2007-prog](https://clawhub.ai/user/yuxiaoyang2007-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract readable content and engagement metadata from X/Twitter links, including long-form X Articles and external pages reached through t.co short links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read authenticated X session material while extracting X Articles.

Mitigation: Run it only in trusted environments and keep access to the xreach session file limited to agents and users that need article extraction.

Risk: External-page extraction can send resolved t.co targets to Firecrawl.

Mitigation: Set FIRECRAWL_API_KEY only when sharing target URLs and retrieved page content with Firecrawl is acceptable; leave it unset to avoid that path.

Risk: The optional ingestion mode can persist extracted material into the content-factory system.

Mitigation: Use --ingest only when the destination and retention of extracted content are intentional.

Risk: Dependencies and proxy configuration can affect execution risk, especially with embedded proxy credentials.

Mitigation: Prefer pinned dependency versions and avoid proxy URLs that include passwords.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuxiaoyang2007-prog/skills/x-article-extract)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [JSON or human-readable text containing extracted content, source metadata, and engagement metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, xreach, and curl. Can optionally resolve t.co links, use an authenticated X session for X Article extraction, call Firecrawl for external pages, and persist extracted material when ingestion is explicitly enabled.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
