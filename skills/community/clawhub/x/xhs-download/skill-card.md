## Description: <br>
小红书笔记批量下载。通过已登录 Chrome 的 DevTools Protocol 自动化下载小红书笔记（图片+文字）到本地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilixiong](https://clawhub.ai/user/weilixiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate guidance, configuration values, shell commands, and a Python script for downloading text and images from selected Xiaohongshu account notes into local folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated workflow controls a logged-in Xiaohongshu Chrome tab through a locally enabled DevTools Protocol debugging session. <br>
Mitigation: Use a separate Chrome profile, keep remote debugging bound to localhost, enable it only while using the skill, and close Chrome afterward. <br>
Risk: The generated script saves note text and images to a local output folder. <br>
Mitigation: Choose a dedicated output folder and download only content you are authorized to keep. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weilixiong/xhs-download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file and folder output when the generated Python script is run by the user.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
