## Description: <br>
Automates Xiaohongshu publishing for text-image and video posts, browser login checks, content search, comments, notification mentions, and creator content data exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[white0dew](https://clawhub.ai/user/white0dew) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, operators, and developers use the skill to operate a logged-in Xiaohongshu Chrome session for preparing or publishing posts, managing accounts, checking login status, searching notes, commenting, reading notifications, and exporting content metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a logged-in Xiaohongshu browser session and publish or comment publicly. <br>
Mitigation: Use a dedicated account or browser profile and manually review each post or comment before allowing publish actions. <br>
Risk: Remote Chrome DevTools Protocol access can expose an authenticated browser session if the endpoint is not private and trusted. <br>
Mitigation: Prefer local CDP on 127.0.0.1 and connect to remote CDP only on private, trusted endpoints. <br>
Risk: The skill can read notification data and export creator content metrics. <br>
Mitigation: Review notification reads, analytics exports, account switches, and profile deletion requests before execution. <br>
Risk: The --auto-publish option can skip the normal manual confirmation point. <br>
Mitigation: Avoid --auto-publish unless the content, account, and publishing intent have already been explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/white0dew/xiaohongshuskills) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [Xiaohongshu creator publish page](https://creator.xiaohongshu.com/publish/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public post actions, comments, notification payload summaries, or CSV exports when the corresponding commands are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
