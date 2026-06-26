## Description: <br>
根据小红书文章内容自动生成配图，使用PIL将文章标题、副标题、内容生成在图片上，适合小红书笔记配图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binsonHao](https://clawhub.ai/user/binsonHao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to generate Xiaohongshu-style cover images from a title, optional subtitle, and optional multi-line body text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script overwrites the fixed output file xhs_cover.jpg in the OpenClaw workspace. <br>
Mitigation: Review the output path before running and preserve any existing image that should not be replaced. <br>
Risk: Image generation depends on Pillow and the referenced CJK font being available in the runtime environment. <br>
Mitigation: Install Pillow and verify the font path before use; inspect fallback-font output when the preferred font is unavailable. <br>
Risk: Generated images may not be publication-ready without human review. <br>
Mitigation: Review the generated image before publishing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binsonHao/redbook-image-generator) <br>
- [Publisher profile](https://clawhub.ai/user/binsonHao) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files] <br>
**Output Format:** [Command-line invocation that writes a JPEG image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pillow and a local CJK font; writes xhs_cover.jpg to a fixed OpenClaw workspace path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
