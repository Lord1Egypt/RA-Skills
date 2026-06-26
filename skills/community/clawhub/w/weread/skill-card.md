## Description: <br>
WeRead (微信读书) lets an agent query a user's bookshelf, reading progress, highlights, notes, reviews, chapters, and local note exports through an authenticated WeRead session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenyqThu](https://clawhub.ai/user/ChenyqThu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent inspect and export their own WeRead reading history, notes, highlights, and reading statistics for search, review, and morning-report workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local WeRead web session cookie and stores it at ~/.weread/cookie, so anyone with access to that file may be able to access the user's WeRead session. <br>
Mitigation: Treat the cookie like a password, keep owner-only file permissions, prefer manual cookie entry or a dedicated browser profile, and delete the cookie when the integration is no longer needed. <br>
Risk: Exported notes and reading history under ~/.weread/ can contain private reading activity, highlights, and annotations. <br>
Mitigation: Do not share exported files unless intended, and delete local exports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub WeRead Skill Page](https://clawhub.ai/ChenyqThu/weread) <br>
- [WeRead Web](https://weread.qq.com) <br>
- [OpenClaw](https://github.com/nicepkg/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; skill scripts emit JSON or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local WeRead cookie and export files under ~/.weread/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
