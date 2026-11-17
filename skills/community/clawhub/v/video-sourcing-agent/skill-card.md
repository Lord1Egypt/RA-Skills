## Description:

Run the Video Sourcing Agent with deterministic, concise chat UX for /video_sourcing using a pinned self-bootstrap runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memories-ai-official](https://clawhub.ai/user/memories-ai-official)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to find, compare, and analyze social videos from services such as YouTube, TikTok, Instagram, and Twitter/X, returning concise conclusions and concrete video references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs downloaded runtime code outside the sandbox while using API keys.

Mitigation: Install only if the Memories.ai Labs runtime is trusted, use restricted API keys, and avoid exposing unrelated secrets in the environment.

Risk: The runtime is fetched from a pinned tag but evidence reports no strong integrity checks.

Mitigation: Review the runtime before deployment and prefer pinning it to an immutable commit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/memories-ai-official/skills/video-sourcing-agent)
- [Video Sourcing Agent Homepage](https://github.com/Memories-ai-labs/video-sourcing-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with concise progress updates, final summary, video references, and tool status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit NDJSON runtime events internally; public responses should include at most the top three video references by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
