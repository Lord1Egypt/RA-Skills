## Description:

Youtube Transcript Fetcher fetches YouTube video transcripts by URL or video ID, with optional language selection and timestamped segments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve YouTube transcripts for summarization, searchable archives, show notes, accessibility workflows, and timestamped citation support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube video identifiers are sent to AgentPMT and transcript JSON is stored behind temporary signed URLs.

Mitigation: Use the skill only when AgentPMT retention and access controls fit the content; avoid sensitive or regulated videos unless approved.

Risk: Remote live instructions and unpinned setup commands may change over time.

Mitigation: Treat live instructions as reference data, review them against local policy, and prefer pinned or reviewed setup commands before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/youtube-transcript-fetcher-newest)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/youtube-transcript-fetcher)
- [Generated action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions with JSON request examples; remote tool responses return JSON transcript file metadata and signed download URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript output is stored as JSON behind a temporary signed URL; timestamped segments and raw provider responses are optional.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
