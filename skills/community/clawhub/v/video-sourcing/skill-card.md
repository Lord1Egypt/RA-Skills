## Description:

Run the Video Sourcing Agent with deterministic, concise chat UX for /video_sourcing using a pinned self-bootstrap runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelz12](https://clawhub.ai/user/samuelz12)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find, compare, and analyze social videos with concrete video links. It is suited for video sourcing, trend analysis, creator analysis, and brand analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically downloads and runs an upstream runtime on the host with Google and YouTube API keys.

Mitigation: Install only if the upstream runtime is trusted, use low-privilege quota-limited API keys, avoid sensitive query text, and review or pin the runtime to an immutable commit before use.

Risk: The skill depends on host tooling and API credentials being available before video sourcing can complete.

Mitigation: Confirm git, uv, GOOGLE_API_KEY, and YOUTUBE_API_KEY are configured in the target environment before invoking the skill.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/samuelz12/skills/video-sourcing)
- [Video Sourcing Agent Repository](https://github.com/Memories-ai-labs/video-sourcing-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Concise chat messages with video links, relevance notes, and compact status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final responses default to a short conclusion, up to three video references, and a compact tools-used summary.]

## Skill Version(s):

0.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
