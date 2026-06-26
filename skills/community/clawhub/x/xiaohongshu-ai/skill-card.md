## Description: <br>
Creates Xiaohongshu promotional images and post copy from a user brief using OpenAI or Volcengine Ark generation, and can publish to Xiaohongshu only when the user explicitly asks it to. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youteacherasia](https://clawhub.ai/user/youteacherasia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agent users use this skill to turn a product, service, event, topic, or personal brief into Xiaohongshu-ready poster images, carousel assets, titles, descriptions, and tags. When deliberately invoked with account credentials, it can publish the generated note to Xiaohongshu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: XHS_COOKIE can act like a logged-in Xiaohongshu account credential. <br>
Mitigation: Keep XHS_COOKIE out of files and version control, provide it only in a controlled runtime environment, and rotate or revoke the cookie when it is no longer needed. <br>
Risk: User descriptions, generated prompts, and marketing content may be sent to external AI providers. <br>
Mitigation: Do not include business secrets, personal data, unpublished product information, or other sensitive content in prompts unless that data transfer has been approved. <br>
Risk: The publishing script can create an actual Xiaohongshu post when deliberately invoked with a valid cookie. <br>
Mitigation: Use --dry-run to validate inputs before publishing, review title, description, and images first, and use --public only when a public post is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youteacherasia/xiaohongshu-ai) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [Volcengine Ark OpenAI-compatible endpoint](https://ark.cn-beijing.volces.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated runs produce PNG image files and a JSON manifest.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image output is intended for Xiaohongshu 3:4 posts; publishing requires an explicit publishing command and XHS_COOKIE.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
