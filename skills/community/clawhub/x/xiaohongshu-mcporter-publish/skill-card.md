## Description: <br>
小红书创作者平台写帖子：mcporter 调用 chrome-devtools-mcp 操作浏览器，禁止 browser 工具。上传图片、填写标题正文，发布由用户手动完成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YEWENWU1](https://clawhub.ai/user/YEWENWU1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and operators use this skill to prepare a Xiaohongshu image post in a browser by uploading local Desktop images and filling the title and body. The final publish action remains manual for the user to review and complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser may be logged into the wrong Xiaohongshu account or use the wrong local image folder. <br>
Mitigation: Verify the active account, inspect the selected Desktop folder and uploaded images, and review the title and body before taking any publish action. <br>
Risk: The skill depends on local mcporter and chrome-devtools-mcp behavior outside the artifact itself. <br>
Mitigation: Install only if you trust your local mcporter and chrome-devtools-mcp setup. Use it with the intended Desktop image folder, verify the browser is logged into the correct Xiaohongshu account, review all uploaded images and text, and publish manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YEWENWU1/xiaohongshu-mcporter-publish) <br>
- [Xiaohongshu creator publishing page](https://creator.xiaohongshu.com/publish/publish?source=official&from=tab_switch) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown guidance with tool and shell command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local mcporter and chrome-devtools-mcp access; publishing is left to manual user action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
