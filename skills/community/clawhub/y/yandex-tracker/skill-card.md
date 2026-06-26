## Description: <br>
Work with Yandex Tracker issues, queues, comments, attachments, links, search, and bulk operations through the Python yandex_tracker_client package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kandler3](https://clawhub.ai/user/Kandler3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external Yandex Tracker users use this skill to let an agent query, create, update, close, comment on, link, attach files to, and bulk-change Tracker issues through Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can change or delete Yandex Tracker data using the account permissions attached to the configured token. <br>
Mitigation: Use a least-privilege or short-lived token and require the agent to show the exact issues, comments, attachments, links, worklogs, transitions, moves, or bulk updates before execution. <br>
Risk: Broad production tokens can expose more Tracker data or mutation capability than a task requires. <br>
Mitigation: Avoid broad admin tokens where possible and scope credentials to the queues and operations needed for the current workflow. <br>


## Reference(s): <br>
- [yandex_tracker_client on PyPI](https://pypi.org/project/yandex-tracker-client/) <br>
- [Yandex Tracker](https://tracker.yandex.ru) <br>
- [Yandex OAuth](https://oauth.yandex.ru) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks, plus structured text summaries from executed scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRACKER_TOKEN and either TRACKER_ORG_ID or TRACKER_CLOUD_ORG_ID; actions run with the token holder's Yandex Tracker permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
