## Description: <br>
Generate professional social media carousel images (Instagram, LinkedIn, TikTok, Xiaohongshu) from text content, articles, or URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangyisheng9-bot](https://clawhub.ai/user/jiangyisheng9-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and agents use this skill to turn text, article links, WordPress posts, or topics into social media carousel slide prompts and generated image files with consistent branding and multilingual support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send carousel prompts, fetched article contents, URLs, and selected product images to Google Gemini for external processing. <br>
Mitigation: Use it only with content and images approved for third-party processing, and avoid confidential drafts, unpublished business material, or private images unless that processing is acceptable. <br>
Risk: The workflow requires a Gemini API key, which is a sensitive credential. <br>
Mitigation: Store the API key outside shared prompts and repositories, provide it only through approved secret-handling paths, and rotate it if exposed. <br>


## Reference(s): <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>
- [Text-to-Carousel on ClawHub](https://clawhub.ai/jiangyisheng9-bot/text-to-carousel) <br>
- [jiangyisheng9-bot publisher profile](https://clawhub.ai/user/jiangyisheng9-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration examples, Python API calls, shell commands, and generated PNG/JPG carousel image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1024x1024 carousel slide images by default; may include prompts and configuration for Gemini image generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
