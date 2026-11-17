## Description:

Generate summaries, highlights, Q&A, presentations, daily digests, and cross-video reviews from YouTube videos using the yt-mem-ai CLI with cached transcripts and semantic search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dasein108](https://clawhub.ai/user/dasein108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content analysts use this skill to ingest YouTube videos or subscription batches through yt-mem-ai and produce transcript-grounded summaries, highlights, Q&A, slide decks, daily digests, and cross-video reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill mandates running an unpinned external yt-mem-ai CLI under the local agent account.

Mitigation: Install only from a trusted yt-mem-ai package source, prefer a pinned and reviewed version, and run in a sandbox where practical.

Risk: The skill can enable Chrome-cookie access and store proxy or API credentials in CLI configuration.

Mitigation: Require explicit approval before enabling browser-cookie access or storing proxy/API credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dasein108/skills/yt-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown responses and files, JSON highlights/Q&A, and shell commands for yt-mem-ai CLI operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write slide, digest, review, and group Markdown files; reuses cached transcripts and summaries when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
