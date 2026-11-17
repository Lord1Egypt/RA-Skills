## Description:

Search academic papers and authors via the Scholar API (scholar.x49.ai) for papers, author profiles, suggestions, metadata, journal rankings, and filters across academic disciplines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahahaaaa123](https://clawhub.ai/user/wahahaaaa123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search scholarly literature, retrieve paper and author metadata, check venue quality signals, and format academic search results for follow-up research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds and automatically uses a shared Scholar API bearer token.

Mitigation: Set a personal SCHOLAR_API_KEY before use and review the shared-key behavior before installing.

Risk: Search terms, filters, and lookup requests are transmitted to scholar.x49.ai.

Mitigation: Avoid confidential or unpublished research queries unless the user accepts that data flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wahahaaaa123/skills/scholar-search-x49)
- [Scholar API documentation](https://scholar.x49.ai/docs?section=api-keys)
- [Scholar API base endpoint](https://scholar.x49.ai/api/v1)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and formatted paper or author result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paper_ref and author_ref identifiers for follow-up lookups.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
