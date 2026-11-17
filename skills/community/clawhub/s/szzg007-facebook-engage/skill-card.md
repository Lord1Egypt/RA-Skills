## Description:

Automates visiting a specified Facebook page, following it, and posting a friendly comment on its latest post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators can use this skill to perform a Facebook follow and leave a positive comment on a selected public page. The user supplies the Facebook URL and may supply the exact comment text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publicly follow pages and post comments from the user's logged-in Facebook account.

Mitigation: Confirm the exact Facebook URL and final comment text before each run, and only proceed when the account owner approves the public action.

Risk: Repeated follows or similar comments may look like spam or violate platform rules.

Mitigation: Use the skill only for limited, intentional engagement and avoid bulk activity or repeated comment text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szzg007/skills/szzg007-facebook-engage)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status report summarizing follow status, target post, submitted comment, and completion state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use browser actions in a logged-in Facebook session and can publicly submit a comment from the user's account.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
