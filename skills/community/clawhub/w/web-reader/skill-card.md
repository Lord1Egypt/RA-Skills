## Description:

Fetches articles and videos from supported web platforms, saves local archives, and supports follow-up summarization, analysis, comparison, and content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexxxiong](https://clawhub.ai/user/alexxxiong)

### License/Terms of Use:

MIT

## Use Case:

Developers and content-focused agent users use this skill to capture web articles, images, and videos into local files, then analyze, summarize, compare, or repurpose the saved material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary web content and save persistent archives locally.

Mitigation: Use explicit trusted URLs, choose a bounded output directory, and review saved files before reusing their contents.

Risk: Some modes can use logged-in browser context or browser cookies for restricted pages.

Mitigation: Avoid cookie-based and private-document modes unless necessary; use a separate browser profile or isolated environment when possible.

Risk: The skill depends on external scraping and downloading tools for article and video capture.

Mitigation: Install pinned dependencies in an isolated environment and review tool behavior before using the skill with sensitive sources.

## Reference(s):

- [Platform Strategies](references/platforms.md)
- [Adding a New Platform](references/extending.md)
- [ClawHub Skill Page](https://clawhub.ai/alexxxiong/skills/web-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON status output, saved article/video files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write persistent local archives and image folders; optional JSON output is available for programmatic use.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
