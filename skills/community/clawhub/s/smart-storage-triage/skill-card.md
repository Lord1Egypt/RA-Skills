## Description:

Universal smart search and storage triage for codebases, local files, documents, and archives. SQLite FTS5 (BM25), gzip tree snapshots, and semantic media search (photos/videos/document names) via local EmbeddingGemma2 embeddings with same-model failover. Requires user confirmation before broad directory indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthet1x](https://clawhub.ai/user/synthet1x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to find relevant code, documents, archived files, photos, and videos across configured local storage, returning focused snippets or paths for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a risk that private or out-of-scope files could enter an index or pass through a configured proxy.

Mitigation: Review the target storage scope and configured router before use; follow the skill's explicit confirmation requirement for broad indexing and opt-in requirement for non-loopback routers.

Risk: The security scan was partial, and some referenced paths could not be matched to bundled files.

Mitigation: Review the unresolved references before installation, as recommended by the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/synthet1x/skills/smart-storage-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, File paths, Search snippets, Configuration guidance]

**Output Format:** [Markdown text with file paths, excerpts, and media search matches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results reflect the configured local indexes and may include relevant excerpts or paths.]

## Skill Version(s):

1.7.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
