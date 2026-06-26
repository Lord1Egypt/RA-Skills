## Description: <br>
知识星球（星球）管理：列出星球、浏览主题、查询标签、搜索成员。当用户需要查看自己加入或创建的星球、浏览星球内容、获取 group_id、查询星球标签或成员时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsxq](https://clawhub.ai/user/zsxq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a logged-in zsxq-cli account for listing Knowledge Planet groups, browsing group topics, viewing hashtags, and searching group members. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may expose private Knowledge Planet account data, including JSON outputs and member search results. <br>
Mitigation: Install and use this skill only when the agent is allowed to read the user's logged-in zsxq-cli account data. <br>
Risk: Raw zsxq-cli api calls can access data beyond the shortcut examples. <br>
Mitigation: Review proposed raw zsxq-cli api calls before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zsxq/zsxq-group) <br>
- [Publisher profile](https://clawhub.ai/user/zsxq) <br>
- [group +list](references/zsxq-group-list.md) <br>
- [group +topics](references/zsxq-group-topics.md) <br>
- [group +hashtags](references/zsxq-group-hashtags.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include group, topic, hashtag, and member data from the user's logged-in Knowledge Planet account.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
