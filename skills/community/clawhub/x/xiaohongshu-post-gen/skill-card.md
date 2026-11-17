## Description:

Generate complete Xiaohongshu (Little Red Book) posts with up to 10 pages in a 3:4 vertical format, auto-parsing text into cover and content pages across four visual styles using Gemini image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:


## Use Case:

Creators, marketers, and agents use this skill to turn supplied Xiaohongshu post text into a multi-page vertical image post with a cover, content pages, quotes, checklists, and an ending page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Gemini API key and sends supplied post text to Gemini for image generation.

Mitigation: Install only where that data sharing is acceptable, avoid sensitive post content, and run the skill in a restricted environment for higher-security use.

Risk: The skill depends on Python packages and writes generated image files locally.

Mitigation: Pin or lock dependencies before use and choose an output directory intended for generated assets.

## Reference(s):

- [Xiaohongshu Post Gen on ClawHub](https://clawhub.ai/franklu0819-lang/skills/xiaohongshu-post-gen)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration]

**Output Format:** [PNG image files and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and writes numbered 3:4 PNG pages to a local output directory.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
