## Description: <br>
Publish text and image posts to Weibo through m.weibo.cn using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to publish text-only or image posts to Weibo from an existing authenticated browser session and verify the result on the profile page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public content from an authenticated Weibo account. <br>
Mitigation: Before sending, confirm the active account, exact post text, attached images, and final Send action. <br>
Risk: Cleanup commands can remove shared temporary or browser media files if used too broadly. <br>
Mitigation: Limit cleanup to files created for the current post and review any broad deletion command before execution. <br>
Risk: The compose page may stay open after publishing, creating a chance of accidental duplicate posts. <br>
Mitigation: Verify the latest post on the profile page, then close the compose tab before considering the workflow complete. <br>


## Reference(s): <br>
- [Workflow Examples](references/workflow-examples.md) <br>
- [Weibo mobile compose page](https://m.weibo.cn/compose) <br>
- [Weibo mobile site](https://m.weibo.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, browser automation commands] <br>
**Output Format:** [Markdown with browser automation steps and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing Weibo login session, manual post verification, and cleanup of temporary upload files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
