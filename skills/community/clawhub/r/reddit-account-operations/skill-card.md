## Description: <br>
Operating doctrine for Reddit account automation with role separation, post qualification, quotas, anti-spam triggers, and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, developers, and operators use this skill to guide scheduled Reddit account workflows where public posting, reputation management, and moderation tolerance matter. It provides operational guidance for configuring accounts, qualifying posts, enforcing quotas, logging activity, and handling blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes anti-CAPTCHA and bot-detection evasion guidance for Reddit posting. <br>
Mitigation: Do not use the evasion workflow; require human approval for posting and follow Reddit and subreddit rules. <br>
Risk: The skill directs an agent to operate a logged-in Reddit profile and make public posts or replies. <br>
Mitigation: Keep a human in the approval loop, verify account state before action, and stop on login, rate-limit, moderation, or challenge signals. <br>
Risk: The skill persists account activity logs and can send optional webhook recaps. <br>
Mitigation: Limit stored and transmitted data to information you are comfortable exposing, and protect webhook destinations and tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/reddit-account-operations) <br>
- [Publisher profile](https://clawhub.ai/user/alexbloch-ia) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with YAML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational guardrails, logging expectations, posting quotas, and recovery steps for a logged-in Reddit browser profile.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
