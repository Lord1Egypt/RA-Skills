## Description: <br>
投票鸭制作助手 helps agents search Toupiaoya voting templates, create voting projects, upload materials, and manage project data through the bundled CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jijun](https://clawhub.ai/user/jijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to build and manage online voting activities with Toupiaoya, including template search, project creation, material upload, vote data retrieval, trend reporting, and option or group management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses X-Openclaw-Token as a local credential. <br>
Mitigation: Treat the token as a secret, avoid sharing ~/.toupiaoya/config.json, and remove that file when persistent login is no longer wanted. <br>
Risk: Project titles, descriptions, options, and uploaded files may be sent to Toupiaoya or Tencent Cloud COS services. <br>
Mitigation: Do not enter secrets, regulated data, or sensitive personal information unless the user is comfortable sending that data to those services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jijun/toupiaoya-creator) <br>
- [Toupiaoya token access](https://www.toupiaoya.com/skillAccess/token) <br>
- [Toupiaoya template search API](https://msearch-api.toupiaoya.com/m/search/searchProducts) <br>
- [Toupiaoya project creation API](https://ai-api.toupiaoya.com/iaigc-toupiaoya/create) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with CLI command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local token configuration and may call Toupiaoya and Tencent Cloud COS services when the user runs the provided commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
