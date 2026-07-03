## Description: <br>
X Helper is a pure Python stdlib assistant for X (Twitter) that can search, post with media, manage threads, direct messages, Lists, bookmarks, trends, articles, follows, blocks, and mutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to drive X account workflows from an agent, including search, posting, media upload, direct messages, Lists, bookmarks, trends, and account relationship actions. It is suited to accounts where the user is comfortable granting OAuth access and confirming write actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad X account-changing actions such as posting, sending DMs, following, blocking, muting, and deleting content. <br>
Mitigation: Use it only with accounts where this level of access is acceptable, and require clear review and confirmation before write actions. <br>
Risk: Tweets, direct messages, media files, search queries, user information, and bearer tokens may be sent to X API services. <br>
Mitigation: Avoid sensitive or confidential DMs, media, and account data when using the skill. <br>
Risk: OAuth credentials are stored durably in ~/.x-helper/auth.json and the security evidence notes an undocumented command that can expose raw bearer tokens. <br>
Mitigation: Protect the auth file, restrict local access, and do not run or expose the get-token command unless raw token handling is intentional. <br>


## Reference(s): <br>
- [X Helper on ClawHub](https://clawhub.ai/tobewin/skills/x-helper) <br>
- [ToBeWin publisher profile](https://clawhub.ai/user/tobewin) <br>
- [X Developer Portal](https://developer.x.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and natural-language action summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python stdlib scripts and requires X OAuth configuration through X_CLIENT_ID or an explicit client ID.] <br>

## Skill Version(s): <br>
3.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
