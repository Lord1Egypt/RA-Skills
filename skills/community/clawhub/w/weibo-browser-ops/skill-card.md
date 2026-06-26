## Description: <br>
Operate Weibo via browser automation for composing posts, publishing content, replying to comments, checking mentions, and monitoring basic account metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YIKAILucas](https://clawhub.ai/user/YIKAILucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Social media operators and account managers use this skill to let an agent manage visible Weibo browser workflows, including drafting posts, replying to mentions or comments, checking notifications, and reviewing basic account metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Weibo account and may affect live posts, replies, deletes, pins, or unpins. <br>
Mitigation: Review the active account, target post or comment, and exact text before approving publish, reply, delete, pin, or unpin actions. <br>
Risk: Login expiry, secondary verification, or CAPTCHA can interrupt browser workflows. <br>
Mitigation: Pause and request user action; do not attempt anti-bot bypass. <br>
Risk: Performance metrics are limited to information visible in Weibo creator pages during the session. <br>
Mitigation: Report only visible stats and label incomplete or unavailable measurements as partial. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/YIKAILucas/weibo-browser-ops) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown operation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports action, account, result, details, and next step when using the artifact output template.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
