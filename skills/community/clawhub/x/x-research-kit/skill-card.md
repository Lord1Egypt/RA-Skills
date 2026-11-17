## Description:

Extracts and analyzes X/Twitter posts, profiles, and Spaces using yt-dlp and gallery-dl for metadata, text, engagement, media, thread, and profile research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuya227939](https://clawhub.ai/user/xuya227939)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, creators, and researchers use this skill to extract structured X/Twitter content and engagement data without an API key. It supports single posts, user timelines, media metadata, Spaces metadata, and local keyword filtering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated X/Twitter extraction may expose browser cookies to command-line tools, and those cookies can act like login credentials.

Mitigation: Use unauthenticated extraction where possible; when cookies are required, use a dedicated browser profile with only the needed X session and avoid logging, storing, or sharing cookie material.

Risk: The workflow depends on local third-party tools, so untrusted or outdated installations can increase supply-chain and execution risk.

Mitigation: Install yt-dlp and gallery-dl from trusted sources, keep them updated or pinned to reviewed versions, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuya227939/skills/x-research-kit)
- [Publisher profile](https://clawhub.ai/user/xuya227939)
- [Project homepage](https://snapvee.com)
- [Support issues](https://github.com/xuya227939/x-research-kit/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and structured tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize JSON fields returned by yt-dlp or gallery-dl; does not directly download media unless the user asks for separate yt-dlp guidance.]

## Skill Version(s):

1.0.0 (source: release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
