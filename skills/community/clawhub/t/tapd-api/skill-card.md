## Description: <br>
TAPD API complete integration covering 18 modules and 70+ API methods with OAuth and Basic Auth support for stories, tasks, bugs, iterations, tests, Wiki, timesheets, and related TAPD workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kailian](https://clawhub.ai/user/kailian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and project teams use this skill to automate TAPD project-management workflows, including querying and updating stories, tasks, bugs, iterations, tests, Wiki entries, timesheets, workspaces, and related records through a Python SDK or shell command interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad remote changes to TAPD project-management data. <br>
Mitigation: Require explicit human approval before create, update, member-add, or bulk-change operations, and start with read-only permissions until write access is needed. <br>
Risk: TAPD OAuth credentials and access tokens can expose project data or write privileges if mishandled. <br>
Mitigation: Use a least-privilege TAPD app, protect tapd.json and ~/.tapd_token_cache.json, set restrictive file permissions, avoid command-line secrets, and rotate credentials regularly. <br>


## Reference(s): <br>
- [ClawHub tapd-api release page](https://clawhub.ai/kailian/tapd-api) <br>
- [TAPD Open Platform](https://open.tapd.cn) <br>
- [TAPD Open Platform API Documentation](https://open.tapd.cn/document/api-doc/) <br>
- [TAPD OAuth Credential Flow](https://open.tapd.cn/document/api-doc/API文档/授权凭证/项目态.html) <br>
- [TAPD API Usage Notes](https://open.tapd.cn/document/api-doc/API文档/使用必读.html) <br>
- [Configuration examples](reference/config-example.md) <br>
- [Usage examples](reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON, Python, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform TAPD API calls through the bundled Python client or shell wrapper when configured with user-provided TAPD credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact metadata reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
