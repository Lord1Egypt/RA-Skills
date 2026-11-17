## Description:

Advanced SEO content creation with AI humanization, image generation, multi-language support, content refresh, SEO scoring, and competitor analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, agencies, and developers use this skill to draft and refresh SEO articles, generate title variants, score content, optimize video metadata, and prepare supporting image-generation prompts or assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes AI-detector bypass language and tooling that could be used to misrepresent AI-generated content.

Mitigation: Use it only for transparent, policy-compliant editing and require human review before publication.

Risk: Image generation can send prompts or input images to an external Gemini API and uses a GEMINI_API_KEY credential.

Mitigation: Keep GEMINI_API_KEY in a protected environment, avoid passing confidential prompts or images, and prefer environment variables over command-line API keys.

Risk: Local output paths can overwrite existing files.

Mitigation: Review target paths before execution and write generated content to a controlled workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly3094/skills/seo-content-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/fly3094)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON reports, generated files, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local article, report, title-test, humanized-text, or image files when invoked with output paths.]

## Skill Version(s):

1.4.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
