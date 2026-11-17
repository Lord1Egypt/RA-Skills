## Description:

TAPD API integration that helps agents use OAuth or Basic Auth to query and manage TAPD workspaces across stories, tasks, bugs, iterations, tests, wiki, timesheets, and related project-management modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kailian](https://clawhub.ai/user/kailian)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to configure TAPD credentials, run TAPD API queries, and generate Python or shell-based project-management operations for TAPD workspaces. It can support both read workflows and write operations such as creating or updating project records when credentials permit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use TAPD credentials with read/write access to configured workspaces.

Mitigation: Use least-privilege TAPD credentials, install only the permissions needed for the intended workflow, and test first in a non-production workspace.

Risk: OAuth tokens may be cached on disk.

Mitigation: Protect the token cache with restrictive file permissions, avoid shared machines, and disable or clear the cache when the workflow does not need persistent tokens.

Risk: Examples include create, update, and bulk update operations that can alter shared project data.

Mitigation: Review generated commands and code before execution, avoid bulk update examples unless the target records are confirmed, and run write operations against a test workspace first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kailian/skills/tapd-api)
- [TAPD open platform](https://open.tapd.cn)
- [TAPD open platform API documentation](https://open.tapd.cn/document/api-doc/)
- [TAPD OAuth credential flow](https://open.tapd.cn/document/api-doc/API文档/授权凭证/项目态.html)
- [TAPD API usage guide](https://open.tapd.cn/document/api-doc/API文档/使用必读.html)
- [TAPD API reference](https://open.tapd.cn/document/api-doc/API文档/)
- [Configuration examples](artifact/reference/config-example.md)
- [Usage examples](artifact/reference/examples.md)
- [Security guidance](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TAPD API request examples, TAPD workspace configuration, and commands or code that perform read/write project-management actions.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
