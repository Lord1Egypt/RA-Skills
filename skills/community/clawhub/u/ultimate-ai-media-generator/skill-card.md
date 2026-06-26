## Description: <br>
Generate AI images and videos with CyberBara models, including text-to-image, text-to-video, image-to-video, and video-to-video workflows with prompt optimization, credit estimation, task polling, and media output handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZeroLu](https://clawhub.ai/user/ZeroLu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate images and videos through CyberBara, prepare visual assets for articles, presentations, social media, marketing, anime, product photography, and storyboard-style workflows, and inspect credits before submitting generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent credential handling stores a CyberBara API key on disk. <br>
Mitigation: Use environment variables or a dedicated low-privilege API key where possible, protect the local credential file, and rotate the key if it may have been exposed. <br>
Risk: Reference images and generation payloads can be uploaded to CyberBara. <br>
Mitigation: Avoid uploading sensitive images or prompts unless CyberBara retention and URL access controls are acceptable for the data. <br>
Risk: Generated files may be saved and opened automatically. <br>
Mitigation: Use --no-open, --no-save, or a controlled output directory when reviewing generated media or running in shared environments. <br>
Risk: The raw command can call authenticated CyberBara API endpoints directly. <br>
Mitigation: Review raw endpoint paths and payloads before execution and limit use to trusted operators. <br>


## Reference(s): <br>
- [Ultimate AI Media Generator Skill Page](https://clawhub.ai/ZeroLu/ultimate-ai-media-generator) <br>
- [CyberBara API Reference](references/cyberbara-api-reference.mdx) <br>
- [AI PPT Workflow](workflows/ai-ppt-skill.md) <br>
- [AI SEO Article Workflow](workflows/ai-seo-article-skill.md) <br>
- [AI Comic Drama Workflow](workflows/ai-comic-drama-skill.md) <br>
- [Curated Prompt Library](workflows/curated-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, CLI commands, JSON API responses, and locally saved generated media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload local reference images, store a CyberBara API key on disk, wait for remote tasks, save generated media under a local output directory, and auto-open saved files unless disabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
