## Description:

Search and analyze videos across YouTube, TikTok, Instagram, and X/Twitter via the Memories.ai Video Searching API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memories-ai-official](https://clawhub.ai/user/memories-ai-official)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search, compare, and analyze social videos across YouTube, TikTok, Instagram, and X/Twitter, returning concrete video references and concise analysis through the Memories.ai API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user video-search queries to the Memories.ai service using a Memories.ai API key.

Mitigation: Install and run it only where sharing those queries with Memories.ai is acceptable, and store MEMORIES_API_KEY as a protected environment variable.

Risk: The skill may fail if the packaged script path, executable permissions, network access, curl, jq, or MEMORIES_API_KEY are unavailable.

Mitigation: Verify the runner script path and permissions before use, and confirm the required tools, environment variable, and network connectivity are available.

Risk: Returned video URLs, metrics, or relevance notes may be incomplete or unavailable from the upstream service.

Mitigation: Show only API-provided video references and metrics, and avoid fabricating URLs or engagement data when fields are missing.

## Reference(s):

- [Memories.ai Video Searching API](https://api-tools.memories.ai/agents/video-searching-api)
- [ClawHub Video Searching skill page](https://clawhub.ai/memories-ai-official/skills/video-searching)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown response with video titles, URLs, platform labels, relevance notes, available metrics, and execution metadata; clarifications and errors are plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMORIES_API_KEY, curl, and jq; sends user video-search queries to Memories.ai and must not fabricate video URLs or metrics.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
