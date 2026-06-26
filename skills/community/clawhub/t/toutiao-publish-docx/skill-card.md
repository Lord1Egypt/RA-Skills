## Description: <br>
用 Cookie 或已保存会话在头条号后台发布文章，支持标题/正文/图片与固定目录 docx 导入。当用户要自动发头条文章、传入 cookie_header 或要求按 docx 流程发布时调用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlesliu-sap](https://clawhub.ai/user/charlesliu-sap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to prepare or publish Toutiao articles from title, body text, optional images, or a fixed-directory docx import workflow. It is suited to controlled publishing sessions where the user can provide a Toutiao cookie header or rely on a saved local session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Toutiao cookie headers and saved sessions can grant account access. <br>
Mitigation: Treat cookie_header values and saved sessions as passwords, avoid logging or sharing them, and install only on hosts you control. <br>
Risk: The workflow can publish article content to a live Toutiao account. <br>
Mitigation: Confirm the target account and article content before setting publish behavior that submits the post. <br>
Risk: Fixed docx and image directories may contain unrelated private files. <br>
Mitigation: Keep watched directories limited to intended publishing assets and remove or archive unrelated files before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlesliu-sap/toutiao-publish-docx) <br>
- [Publisher profile](https://clawhub.ai/user/charlesliu-sap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local article, image, docx, screenshot, and session artifact paths used by the publishing workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
