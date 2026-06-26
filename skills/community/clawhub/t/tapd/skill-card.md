## Description: <br>
Tapd helps an agent query, create, and update TAPD requirements, tasks, defects, comments, workflows, iterations, test cases, Wiki pages, timesheets, release plans, and optional enterprise WeChat notifications through TAPD Open API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KevinDai](https://clawhub.ai/user/KevinDai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to let an agent operate TAPD work items and related project records on their behalf. It is useful when users need TAPD lookups, updates, comments, Wiki edits, time logging, release-plan queries, or TAPD-linked notifications from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change TAPD work items, comments, Wiki content, time logs, and related project records. <br>
Mitigation: Use least-privilege TAPD credentials and require clear user confirmation before write operations. <br>
Risk: Custom TAPD API base URLs or webhook URLs could send requests to an unintended endpoint. <br>
Mitigation: Verify TAPD_API_BASE_URL and BOT_URL before use and keep webhook URLs private. <br>


## Reference(s): <br>
- [TAPD](https://www.tapd.cn) <br>
- [TAPD API Reference](artifact/reference/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/KevinDai/tapd) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TAPD credentials from environment variables and can call TAPD or a configured enterprise WeChat webhook.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
