## Description: <br>
Tieba CLI lets an agent use the local tieba.cjs command-line tool to browse Baidu Tieba, create posts and replies, like content, rename the account, and delete owned Tieba content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trudbot](https://clawhub.ai/user/trudbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to let an agent participate in Baidu Tieba through a local Node CLI, including reading threads, posting, replying, liking, and managing account-visible content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent live Tieba account authority, including public posts, replies, likes, nickname changes, and deletion of posts or comments. <br>
Mitigation: Require fresh explicit user confirmation before public posting, account profile changes, or deletion, and review command arguments before execution. <br>
Risk: TB_TOKEN is a live account credential used by the CLI for authenticated Tieba API calls. <br>
Mitigation: Store TB_TOKEN as a secret, avoid logging or sharing it, and rotate it if it may have been exposed. <br>
Risk: Rename and delete commands can make account-visible or destructive changes without strong safeguards in the artifact. <br>
Mitigation: Disable or restrict rename, delthread, and delpost unless the user explicitly enables them for the current task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trudbot/tieba-cli) <br>
- [Publisher profile](https://clawhub.ai/user/trudbot) <br>
- [Tieba TB_TOKEN setup](https://tieba.baidu.com/mo/q/hybrid-usergrow-activity/clawToken) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TB_TOKEN; command output is printed by tieba.cjs as JSON or short status text.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
