## Description: <br>
Enables an agent to use ZenTao RESTful API v2.0 for project-management workflows across programs, products, projects, executions, requirements, bugs, tasks, tests, releases, feedback, tickets, users, and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catouse](https://clawhub.ai/user/catouse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, and automation agents use this skill to inspect and update ZenTao project data through authenticated REST API calls. It supports common work items such as projects, executions, requirements, bugs, tasks, test cases, builds, releases, feedback, tickets, users, and files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles ZenTao account tokens and may cache long-lived credentials in ~/.zentao-token.json. <br>
Mitigation: Use HTTPS-only ZenTao URLs, prefer limited-scope or revocable credentials when available, restrict the cache file to the local user, and remove the cache when switching accounts or decommissioning access. <br>
Risk: The skill can perform write, delete, and state-transition operations against project-management records. <br>
Mitigation: Confirm write and bulk operations before execution, review generated request payloads, and use an account with only the permissions needed for the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/catouse/zentao-api) <br>
- [Publisher profile](https://clawhub.ai/user/catouse) <br>
- [Source repository from release metadata](https://github.com/easysoft/zentao-skills.git) <br>
- [ZenTao API v2.0 documentation](https://www.zentao.net/book/api/2309.html) <br>
- [ZenTao API v1.0 documentation](https://www.zentao.net/book/api/1397.html) <br>
- [Bundled ZenTao API endpoint reference](api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ZenTao URL, token, account, and optional password environment variables; may cache URL, token, and account in ~/.zentao-token.json.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
