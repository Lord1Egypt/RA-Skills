## Description: <br>
Monitors Tom Doerr's X.com profile for new posts, verifies GitHub links, prepares Brazilian Portuguese social copy, requests Telegram approval, and can post approved updates to Twitter/X. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gbrokng](https://clawhub.ai/user/gbrokng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who monitor Tom Doerr's X.com activity can use this skill to check for new GitHub repository posts, verify destination links, rewrite updates in Brazilian Portuguese, request Telegram approval, and publish approved posts from a logged-in X account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run hourly and publish public social posts from a logged-in X account with limited built-in controls. <br>
Mitigation: Before enabling cron, confirm the exact X account, change the Telegram recipient to an account the operator controls, require review of every rewritten post before approval, and keep a clear way to disable the recurring job. <br>
Risk: Posts may share broken or misleading GitHub links if X displays truncated or redirected URLs. <br>
Mitigation: Verify each repository link through the actual t.co redirect or by searching GitHub before drafting or approving a post. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gbrokng/twitterbrowserpost) <br>
- [Tom Doerr X profile](https://x.com/tom_doerr) <br>
- [X post composer](https://x.com/compose/post) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown workflow with inline shell commands and drafted social post text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user approval before public posting and uses a browser profile logged into the target X account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
