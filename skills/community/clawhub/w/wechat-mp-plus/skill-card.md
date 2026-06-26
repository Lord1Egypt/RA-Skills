## Description: <br>
Automate WeChat Official Account management with draft publishing, menu editing, auto-reply checking, and Markdown-to-HTML formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who control a WeChat Official Account use this skill to prepare article drafts, manage custom menus, inspect auto-reply settings, and convert Markdown content into WeChat-compatible HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a live WeChat Official Account, including creating or deleting drafts and menus. <br>
Mitigation: Use it only with accounts you control, review generated commands before execution, and verify target media IDs or menu payloads before destructive operations. <br>
Risk: WeChat AppID, AppSecret, the .secrets file, and the temporary access-token cache are sensitive credentials. <br>
Mitigation: Use an isolated environment, restrict file access, avoid sharing logs or cache files, and rotate credentials if exposure is suspected. <br>
Risk: The Markdown conversion script may install the markdown dependency into the active Python environment. <br>
Mitigation: Preinstall dependencies in a dedicated virtual environment before running the skill. <br>


## Reference(s): <br>
- [ClawHub listing for WeChat MP Plus](https://clawhub.ai/huuuwnnn-droid/wechat-mp-plus) <br>
- [Publisher profile: huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and CLI-oriented shell commands; bundled scripts emit status text, JSON identifiers, and WeChat-compatible HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat Official Account credentials and can change live account resources such as drafts, uploaded media, and custom menus.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
