## Description: <br>
Automates publishing a Sina Weibo post from a logged-in browser session when the user asks to post to Weibo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinazkk](https://clawhub.ai/user/chinazkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to post content to Sina Weibo through browser automation, including emoji and topic tags. The skill is intended for a logged-in browser profile and requires careful review of the exact post before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish publicly from a logged-in Weibo browser profile without a required final approval step. <br>
Mitigation: Require a final confirmation that shows the exact account and exact post text before clicking send. <br>
Risk: Topic tags may be posted incorrectly if they do not use the required #tag# format. <br>
Mitigation: Validate topic tags before publishing and ask the user to correct malformed tags. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinazkk/weibo-post) <br>
- [Weibo](https://weibo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, browser automation commands, guidance] <br>
**Output Format:** [Browser automation tool calls with concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes to the active logged-in Weibo account; Markdown formatting is treated as plain text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
