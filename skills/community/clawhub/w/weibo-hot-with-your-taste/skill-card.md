## Description: <br>
Fetches Weibo trending topics, filters and summarizes them according to user preferences, pushes tailored updates, and adapts taste rules from feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zify9000](https://clawhub.ai/user/zify9000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a personalized Weibo trends monitor that fetches, filters, summarizes, and pushes topics through Feishu while learning from feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses LLM API keys, Feishu credentials, and Weibo session cookies in local environment files. <br>
Mitigation: Use dedicated least-privilege credentials, keep environment files out of shared workspaces and repositories, and restrict file permissions. <br>
Risk: Recurring scheduled workflows can fetch and push content with limited human oversight. <br>
Mitigation: Review scripts and scheduled commands before enabling recurrence, use a separate Weibo account where practical, and monitor logs and pushed content. <br>


## Reference(s): <br>
- [Source repository](https://github.com/zify9000/weibo-hot-with-your-taste) <br>
- [ClawHub listing](https://clawhub.ai/zify9000/skills/weibo-hot-with-your-taste) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON/status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce Feishu card messages and local environment, configuration, log, and JSONL data files when its scripts are executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
