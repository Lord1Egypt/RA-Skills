## Description: <br>
Generates WeChat public account article HTML from Markdown and can upload the result to a configured WeChat draft folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangchao228](https://clawhub.ai/user/yangchao228) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to convert Markdown articles into WeChat-compatible HTML with consistent typography, then optionally publish the generated article as a WeChat draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes real-looking WeChat credentials and can upload user article content to an unclear configured account. <br>
Mitigation: Replace the bundled WeChat credentials with credentials for the intended official account, confirm the draft destination before upload mode, and rotate the exposed app secret if it belongs to you. <br>
Risk: Markdown content and optional images may be sent to WeChat APIs during upload mode. <br>
Mitigation: Avoid uploading confidential Markdown or images unless the WeChat account, credentials, and data handling expectations have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/yangchao228/wx-md-article) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated HTML output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can write HTML and temporary JSON files locally, and upload article content or images to WeChat APIs when upload mode is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
