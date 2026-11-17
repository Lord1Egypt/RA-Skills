## Description:

Search, retrieval, or knowledge-base intent when the user does not clearly mean local files only or the open web: curl a remote RAGret API for semantic retrieval with provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sugarsong404](https://clawhub.ai/user/sugarsong404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route knowledge-base search requests to a configured RAGret service, list accessible indexes, retrieve ranked passages, and cite returned sources when useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys and sensitive search queries to a configured RAGret endpoint that may be unvalidated or plaintext.

Mitigation: Confirm the base URL before use, prefer HTTPS for non-local services, use a least-privilege API key, and avoid sending confidential queries to unknown endpoints.

Risk: Search results are retrieved from the configured knowledge base and may be incomplete, stale, or outside the user's intended retrieval scope.

Mitigation: Clarify whether the user wants RAGret, open-web search, or local-file search before calling the API, and cite returned sources when useful.

## Reference(s):

- [RAGret project](https://github.com/SugarSong404/RAGret.git)
- [ClawHub skill page](https://clawhub.ai/sugarsong404/skills/ragret-search)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline bash commands and retrieved text or JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output depends on the configured RAGret endpoint, selected index, API-key permissions, and returned source metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
