## Description: <br>
Generates PNG card images, cover images, text posters, WeChat article covers, X-style post share images, and long social-post images from user-provided copy or post data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aatrooox](https://clawhub.ai/user/aatrooox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content operators use this skill to turn short copy, long articles, WeChat cover text, or social-post data into polished PNG images for sharing and reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python scripts and headless Chrome to render images. <br>
Mitigation: Install only when comfortable with local script and browser execution; review generated commands before running them. <br>
Risk: Generated image output can be written to user-supplied paths. <br>
Mitigation: Prefer workspace-relative output paths and avoid writing into sensitive or unexpected directories. <br>
Risk: Untrusted Markdown, HTML-like text, icons, or avatars may be rendered in a browser. <br>
Mitigation: Use trusted source content and avoid passing sensitive local files as icons or avatars. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aatrooox/z-card-image) <br>
- [Poster 3:4 template specification](references/poster-3-4.md) <br>
- [Article 3:4 template specification](references/article-3-4.md) <br>
- [X-like posts template specification](references/x-like-posts.md) <br>
- [Tweet thread compatibility notes](references/tweet-thread.md) <br>
- [WeChat cover split template specification](references/wechat-cover-split.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python shell commands that render PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG files at user-specified output paths; some flows read JSON post data or Markdown/text files as inputs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
