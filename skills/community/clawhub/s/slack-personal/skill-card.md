## Description: <br>
Read, send, search, and manage Slack messages and DMs via the slk CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent check Slack activity, read channels and DMs, search messages, manage drafts, and send or react to Slack messages through the local slk CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses and caches sensitive Slack session credentials from the logged-in desktop session. <br>
Mitigation: Install only when this access is intended, prefer one-time Keychain Allow over Always Allow, and delete ~/.local/slk/token-cache.json to clear the cached Slack token. <br>
Risk: The skill can read private Slack channels and DMs and can post as the logged-in user. <br>
Mitigation: Use it only in workspaces where agent access is appropriate, review outbound messages or drafts before sending, and limit use on sensitive conversations. <br>
Risk: Shared or managed machines increase the chance that another local process can trigger Slack credential extraction. <br>
Mitigation: Avoid installing or using the skill on shared or managed machines unless local credential access is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/therohitdas/slack-personal) <br>
- [slkcli npm Package](https://www.npmjs.com/package/slkcli) <br>
- [Slack API](https://slack.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Slack CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Slack channel names, message excerpts, timestamps, draft instructions, or send/react commands depending on the user request.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
