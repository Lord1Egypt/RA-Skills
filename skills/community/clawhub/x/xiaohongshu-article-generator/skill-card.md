## Description: <br>
小红书图文生成技能 - 基于热点话题自动生成小红书风格的图文内容（文案 +HTML+ 图片） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiker1996](https://clawhub.ai/user/shiker1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and agent users use this skill to turn a topic or trend into Xiaohongshu-style copy, mobile HTML pages, and PNG image assets for review and publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and overwrite files in its configured output directory. <br>
Mitigation: Use a dedicated workspace and keep outputDir values scoped to the intended project directory. <br>
Risk: The skill may use browser rendering or browser access while generating image assets or trend-informed content. <br>
Mitigation: Run it in a controlled environment and review generated HTML and PNG files before publishing. <br>
Risk: Generated social content may include inaccurate, sensitive, or unsuitable claims if the input topic or source context is weak. <br>
Mitigation: Review copywriting and images for accuracy, compliance, attribution, and publication suitability before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shiker1996/xiaohongshu-article-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/shiker1996) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance, generated HTML, copywriting Markdown, and PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a topic-specific output directory containing HTML, copywriting.md, and rendered page images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
