## Description:

Generates AI images and videos through CyberBara models such as Sora 2, Kling 2.6, Seedance 2.0, Nano Banana Pro, and Veo 3.1, with prompt optimization, credit estimates, task polling, and media output handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerolu](https://clawhub.ai/user/zerolu)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and agent users use this skill to generate images and videos, quote CyberBara credit costs before submission, poll generation tasks, and save resulting media for content, presentation, SEO, social, and storyboard workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer path may install moving code if the source revision is not pinned.

Mitigation: Review the artifact before installation and pin the installer input to a trusted repository revision.

Risk: API keys can be provided on the command line or saved to a local cache file.

Mitigation: Prefer CYBERBARA_API_KEY or a secret manager, restrict permissions on saved keys, and rotate keys if exposure is suspected.

Risk: Generated media files are saved and opened by default, which may launch untrusted local files.

Mitigation: Use --no-open unless the generated output source and file type are trusted.

Risk: The raw command can call arbitrary CyberBara API endpoints.

Mitigation: Avoid raw unless the exact endpoint, method, and payload have been reviewed.

## Reference(s):

- [CyberBara API Reference](references/cyberbara-api-reference.mdx)
- [AI PPT Workflow](workflows/ai-ppt-skill.md)
- [AI SEO Article Workflow](workflows/ai-seo-article-skill.md)
- [AI Comic Drama Workflow](workflows/ai-comic-drama-skill.md)
- [Curated Prompt Library](workflows/curated-prompts.md)
- [CyberBara](https://cyberbara.com)
- [CyberBara Credit Costs](https://cyberbara.com/credit-costs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task, status, URL, and saved-file outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated image or video files to media_outputs/ and auto-open them unless disabled.]

## Skill Version(s):

1.0.1 (source: server release metadata; changelog source: user, released 2026-03-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
