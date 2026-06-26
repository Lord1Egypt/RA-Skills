## Description: <br>
Manage X (Twitter) accounts: post tweets, like, reply, retweet, view timeline, search, auto-interact, and analyze data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage X/Twitter account activity, including posting, engagement, timeline retrieval, and search through configured user credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local credential files can expose X/Twitter API tokens. <br>
Mitigation: Store credentials only in protected local paths, avoid committing per-user credential files, and rotate tokens if exposure is suspected. <br>
Risk: The skill can post, reply, like, retweet, or auto-reply without built-in confirmation. <br>
Mitigation: Require human approval before any account-changing action, especially automated replies or engagement. <br>
Risk: An unrestricted agent could act with credentials for the wrong USER_ID. <br>
Mitigation: Restrict which USER_ID values an agent can use and run the skill only in a trusted, isolated environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/patches429/storyclaw-x-manager) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/patches429) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python scripts that call X/Twitter API endpoints with user-scoped credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
