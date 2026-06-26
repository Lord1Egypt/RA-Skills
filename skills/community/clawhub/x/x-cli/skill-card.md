## Description: <br>
Full-featured X/Twitter toolkit: read, search, post, interact, DMs, lists, polls, and trends with cookie authentication and no API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ignsoftwarellc](https://clawhub.ai/user/ignsoftwarellc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to let an agent read X/Twitter content, search timelines, publish posts, manage interactions, handle DMs, and perform account operations from command-line tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live control over an X/Twitter account, including posting, DMs, deletion, follows, blocks, lists, uploads, polls, and scheduled actions. <br>
Mitigation: Require explicit user approval before any state-changing action and prefer a dedicated account for agent use. <br>
Risk: Authentication uses account credentials and cookies, which can expose the account if copied into chat, command history, logs, or shared files. <br>
Mitigation: Do not paste passwords into chat, avoid command-line password flags, and protect config.json and cookies.json with local file controls. <br>
Risk: Automated public posts, DMs, or moderation actions can be reputationally or operationally harmful if triggered unintentionally. <br>
Mitigation: Use dry-run or preview flows where available and require confirmation for post, DM, delete, follow, block, upload, poll, list, and schedule commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ignsoftwarellc/x-cli) <br>
- [X-CLI project homepage](https://github.com/ignsoftwarellc/x-cli) <br>
- [twikit library](https://github.com/d60/twikit) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text by default, with optional structured JSON from command flags and inline shell commands in usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read live account state or perform live X/Twitter account actions depending on the selected script and user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
