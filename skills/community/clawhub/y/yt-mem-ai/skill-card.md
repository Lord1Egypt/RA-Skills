## Description:

Runs the yt-mem-ai CLI to ingest YouTube videos, discover subscription uploads, search and manage a local video library, rate and recommend videos, compile highlights, build supercuts, and coordinate analysis through the related yt-agent skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dasein108](https://clawhub.ai/user/dasein108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate the yt-mem-ai YouTube pipeline from an agent session, including ingestion, transcript retrieval, library search, recommendations, highlight compilation, supercut generation, status checks, and routine subscription processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to run the latest yt-mem-ai package from a registry.

Mitigation: Review the package source and release before use, and only run it in environments where executing registry-provided CLI code is acceptable.

Risk: The skill can configure browser-cookie access or Webshare credentials for YouTube fetch recovery.

Mitigation: Enable those options only when needed, prefer a dedicated browser profile, keep secrets out of version control, and remove credentials when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dasein108/skills/yt-mem-ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce file paths for digests, compilations, supercuts, frames, and related sidecar files when CLI operations create artifacts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
