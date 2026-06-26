## Description: <br>
自动化搬运小红书笔记到 Facebook 和 WordPress，包括文本提取、图片处理、上传准备和发布步骤。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilixiong](https://clawhub.ai/user/weilixiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators use this skill to transfer Xiaohongshu note text and images into Facebook and WordPress publishing workflows for accounts and destinations they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content to live Facebook and WordPress destinations with weak confirmation and scoping controls. <br>
Mitigation: Use it only for destinations you control, verify account and site IDs before posting, prefer drafts or explicit confirmation before publish, and review the upload directory contents before any live upload. <br>
Risk: The GUI upload automation can select unintended files or operate on the wrong macOS file dialog. <br>
Mitigation: Run GUI automation only when the target file dialog is visibly correct, and clear and inspect /tmp/openclaw/uploads before each upload. <br>
Risk: WordPress publishing depends on a bearer token with posting authority. <br>
Mitigation: Use a least-privilege token, keep it in the WP_TOKEN environment variable, and rotate or revoke it if exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weilixiong/xiaohongshu-transfer) <br>
- [Platform configuration](references/platforms.md) <br>
- [Pitfalls and safeguards](references/pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, AppleScript, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local image files, temporary upload directories, and WordPress API requests when the user executes the generated steps or bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
