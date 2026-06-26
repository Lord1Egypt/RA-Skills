## Description: <br>
通过浏览器操作网页版微博，用户登录后 Agent 撰写内容并自动发布。无需 API，需 Browser Relay 挂上微博标签页。Keywords: 微博, 发微博, 自动发布, Weibo, ZeeLin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to draft and publish posts to a logged-in Weibo account through the Weibo web interface when Browser Relay is attached to the intended tab. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public Weibo posts from a logged-in account without a built-in final approval step. <br>
Mitigation: Require the agent to show the exact post text and wait for explicit final approval before executing the publish command. <br>
Risk: Browser Relay or browser automation could act on the wrong Weibo tab or account if attached incorrectly. <br>
Mitigation: Keep Browser Relay attached only to the intended Weibo page, confirm the logged-in account before use, and detach it after publishing. <br>
Risk: Troubleshooting snapshots may include sensitive page content. <br>
Mitigation: Delete /tmp/weibo_snap.txt after troubleshooting and avoid sharing it unless sensitive content has been reviewed or removed. <br>


## Reference(s): <br>
- [Weibo](https://weibo.com) <br>
- [ClawHub release page](https://clawhub.ai/kelcey2023/zeelin-weibo-autopost) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local browser automation against a logged-in Weibo tab and may write a troubleshooting snapshot to /tmp/weibo_snap.txt.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
