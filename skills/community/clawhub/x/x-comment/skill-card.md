## Description:

Automates browsing the X home timeline to select technology and BTC-related posts and publish concise replies from a logged-in profile without liking posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social-media operators use this skill to have an agent browse a logged-in X home timeline, select technology or BTC-related posts, generate concise comments, and publish public replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public replies from a logged-in X/Twitter account without confirmation.

Mitigation: Install only for accounts where automated public replies are acceptable; restrict topic scope and review account-level posting permissions before use.

Risk: The evidence notes ambiguous like-action behavior even though the release summary says the skill only comments.

Mitigation: Review the skill before deployment and disable any like-related steps so the agent only posts replies.

Risk: Optional follow-up tracking can create persistent engagement history and repeated revisits.

Mitigation: Disable follow-up tracking unless explicitly needed, and tightly control retention and access for any saved engagement state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mars82311111/skills/x-comment)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser-action JSON and JavaScript snippets; generated X replies are plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated replies are constrained to 280 characters and language-matched to the original post.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
