## Description: <br>
提取公开 Tower 项目和公告页的标题、作者、更新时间、任务状态及文档资源等信息并进行摘要整理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use Tower to summarize public Tower announcement and project pages, extracting page metadata, task grouping and status counts, and resource links for internal analysis or reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user could provide a Tower link that is not genuinely public or is not approved for summarization. <br>
Mitigation: Use only genuinely public Tower links and confirm that the team or organization allows summarizing those pages. <br>
Risk: Dynamic Tower pages may be summarized before all public content is fully rendered. <br>
Mitigation: Wait for page rendering to complete before extracting titles, authors, timestamps, body summaries, task groups, statuses, or resource links. <br>


## Reference(s): <br>
- [Tower homepage](https://tower.im/) <br>
- [ClawHub skill page](https://clawhub.ai/codenova58/tower) <br>
- [Publisher profile](https://clawhub.ai/user/codenova58) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and structured lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Only public Tower pages are in scope; the skill does not perform account login or task-changing actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
