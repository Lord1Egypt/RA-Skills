## Description: <br>
Automates Twitter/X web posting through browser tools, including trending-topic discovery, post drafting, and publishing with either automatic or manual confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to draft and publish posts from a logged-in X/Twitter browser session, including direct user-provided posts or posts generated from selected trending topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish agent-written public posts from a logged-in X/Twitter account without final confirmation. <br>
Mitigation: Prefer manual confirmation and review the exact post before publishing, especially for reputationally sensitive accounts. <br>
Risk: Broad requests such as fully automatic trend selection plus posting can create account and reputation risk. <br>
Mitigation: Use a dedicated or low-risk account and avoid fully automatic posting unless the user accepts those consequences. <br>
Risk: Repeated automated posting may trigger platform controls or produce unwanted posts. <br>
Mitigation: Limit posting frequency, stop after a small number of failed attempts, and ask the user to retry after confirming account state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/twitter-web-autopost) <br>
- [X compose page](https://x.com/compose/tweet) <br>
- [X trends page](https://x.com/explore/tabs/trending) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown or plain text status with the final post text and resulting post URL when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate a browser session and publish a public post from the user's logged-in X/Twitter account.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
