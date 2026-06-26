## Description: <br>
Generate educational comic-style Xiaohongshu posts using AI-generated comic images, including topic research, storyboard creation, image generation, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizonzzzz](https://clawhub.ai/user/horizonzzzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators and agent users use this skill to turn a chosen topic into an educational Xiaohongshu comic post with researched talking points, Chinese dialogue, generated comic images, title, body text, hashtags, and optional publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish to a Xiaohongshu account using stored login cookies. <br>
Mitigation: Keep the cookie file private and require explicit approval of the final title, body, hashtags, and image paths before publishing. <br>
Risk: The workflow depends on external API keys and companion skills for search, image generation, browser automation, and Xiaohongshu publishing. <br>
Mitigation: Review installed dependency skills, configure only the required credentials, and limit credential exposure to the agent workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horizonzzzz/xhs-comic-creator) <br>
- [Workflow](references/workflow.md) <br>
- [Comic generation rules](references/comic_generation.md) <br>
- [Xiaohongshu posting guidance](references/xhs_posting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, generated post copy, image file paths, and publishing parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a title, body text, 5-6 comic images, hashtags, and Xiaohongshu publishing inputs.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
