## Description: <br>
Simulates login to qinglite.cn to retrieve a token, or uses an existing token to publish user-provided content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccf22222](https://clawhub.ai/user/ccf22222) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to authenticate to qinglite.cn with SMS credentials and publish articles, text, images, or videos through qinglite.cn using a token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The login flow can print an authentication token to terminal output. <br>
Mitigation: Treat the returned token like a password and avoid running the login flow where terminal output is logged or shared. <br>
Risk: A valid token authorizes publishing content to the user's qinglite.cn account. <br>
Mitigation: Review the title, content, type, and media fields before sending a publish request. <br>


## Reference(s): <br>
- [ClawHub qinglite Skill Page](https://clawhub.ai/ccf22222/qinglite) <br>
- [qinglite.cn Login API](https://www.qinglite.cn/api/interface/user/user_mobile/login) <br>
- [qinglite.cn Publish API](https://www.qinglite.cn/api/interface/content/news/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text status messages and token strings from Python command-line execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Login output can include an authentication token; publish output reports success or failure.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
