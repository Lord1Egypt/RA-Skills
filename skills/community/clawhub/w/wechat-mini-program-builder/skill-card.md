## Description: <br>
AI-assisted tool to quickly build WeChat Mini Programs with templates, generated page code, cloud function templates, and deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small businesses use this skill to scaffold WeChat Mini Program projects, generate page code from prompts, create common cloud function templates, and follow setup and deployment steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup instructions reference a global npm installation that the security scan says should not be automatically trusted. <br>
Mitigation: Independently verify the referenced npm package before installing it globally, or test it only in a disposable environment. <br>
Risk: The helper script writes files and directories based on user-provided names. <br>
Mitigation: Run it only in a disposable project directory and use simple non-path project, page, and function names. <br>
Risk: AI page generation sends prompt content to an external OpenClaw API client. <br>
Mitigation: Do not include secrets, customer data, internal URLs, or proprietary requirements in generation prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/wechat-mini-program-builder) <br>
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated WeChat Mini Program code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write project directories, page markdown, cloud function JavaScript, and package.json files when its helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
