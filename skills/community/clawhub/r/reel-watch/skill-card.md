## Description:

Analyzes user-provided videos or images with Gemini or local frames and transcription, then reports the tools, links, repositories, and commands shown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hnf-frn](https://clawhub.ai/user/hnf-frn)

### License/Terms of Use:

MIT-0

## Use Case:

Users and their agents use this skill to inspect social-media or local videos and screenshots, then summarize the workflow and identify tools, links, repositories, and commands shown without executing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When a Gemini key is configured, user-provided media, captions, and screenshots may be sent to Google Gemini.

Mitigation: Use --engine local or omit GEMINI_API_KEY for sensitive content.

Risk: Authenticated Instagram fetching can use cookies when REEL_IG_COOKIES is supplied.

Mitigation: Leave REEL_IG_COOKIES unset unless authenticated fetching is intentional.

Risk: Video content and generated analysis may contain unsafe instructions or misleading commands.

Mitigation: Treat the content as untrusted; review commands with the user before executing them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hnf-frn/skills/reel-watch)
- [Project homepage (listed in skill metadata)](https://github.com/HNF-FRN/Reel-watcher-telegram-Agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown video breakdown and plain-text analysis summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves a breakdown and index under reels/; includes frame paths and a transcript when available.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
