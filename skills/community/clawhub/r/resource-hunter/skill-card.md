## Description:

Find the best public route to pan links, magnets, torrents, and public video URLs for movies, TV, anime, music, software, and books.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mnbplus](https://clawhub.ai/user/mnbplus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search public no-API sources for candidate pan links, magnets, torrents, and public video URLs, then triage results by direct, actionable, and clue semantics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetch logic can let untrusted search results drive requests to unexpected destinations.

Mitigation: Review before installing in environments with access to private intranet, cloud metadata, or loopback-only services.

Risk: Returned pan, torrent, magnet, and video links are external public content and may be unsafe or misleading.

Mitigation: Treat returned links as untrusted and inspect them before opening, downloading, or sharing.

Risk: Public HTML, RSS, and search-index sources can drift, throttle, block, or vary by region.

Mitigation: Use source health checks, review warnings in output, and verify high-impact results before relying on them.

Risk: Dalipan currently produces token-only clue records rather than guaranteed final share URLs.

Mitigation: Present Dalipan records as follow-up clues and avoid describing them as completed direct links.

## Reference(s):

- [Resource Hunter ClawHub Page](https://clawhub.ai/mnbplus/skills/resource-hunter)
- [mnbplus Publisher Profile](https://clawhub.ai/user/mnbplus)
- [README](README.md)
- [Source Matrix](references/sources.md)
- [Architecture](references/architecture.md)
- [Usage Notes](references/usage.md)
- [Release Notes 2.1.1](artifacts/RELEASE-NOTES-2.1.1.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include direct, actionable, or clue-only records; returned external links should be treated as untrusted content.]

## Skill Version(s):

2.1.1 (source: frontmatter, pyproject.toml, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
