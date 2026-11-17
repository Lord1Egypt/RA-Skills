## Description:

清华网络学堂（learn.tsinghua.edu.cn）自动化。要求用户提供网络学堂登录密码（本地 DPAPI 加密存储），自动登录、查看待办、下载课件、提交作业、批量标记已读。当需要操作网络学堂完成日常学习任务时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT-0

## Use Case:

Students and agents use this skill to automate routine Tsinghua Learn tasks such as login, todo review, courseware download, homework submission, PDF preparation, cleanup, and marking notices or files as read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Tsinghua Learn login and stores local credentials, browser profile data, and session files.

Mitigation: Install only if the publisher is trusted, protect the local account and skill directory, and clear stored account state when the skill is no longer needed.

Risk: The skill can change account state, including marking notices or files as read during todo checks.

Mitigation: Disable automatic mark-read unless that behavior is intended, and review account-changing actions before allowing the agent to execute them.

Risk: Plaintext temporary credential workflows can expose account secrets.

Mitigation: Avoid workflows that place credentials in plaintext temporary files and remove any temporary credential material immediately after initialization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomuiv/skills/tsinghua-learn)
- [Tsinghua Learn](https://learn.tsinghua.edu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON-backed status summaries, shell command execution, configuration updates, and generated or downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows and CAS_PASSWORD; stores local login, browser profile, and session state for Tsinghua Learn automation.]

## Skill Version(s):

1.0.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
