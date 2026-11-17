## Description:

Search and analyze X/Twitter posts, comments, creator profiles, post lists, and replies written by creators, including self-replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

People researching X/Twitter conversations and creators can search posts, inspect post details and discussions, view creator profiles and post lists, and review creator-authored replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary marks the skill suspicious because it repeatedly runs an unpinned, changing SocialDataX CLI package, creating supply-chain exposure involving credentials and local access.

Mitigation: Avoid installation until the CLI is pinned to a reviewed version and its integrity is checked.

Risk: Queries or URLs may be sent to SocialDataX, and the available skill scan is partial.

Mitigation: Use only with queries or URLs you are comfortable sending to SocialDataX, and account for the incomplete security evidence when reviewing the release.

## Reference(s):

- [SocialDataX API access and product information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub release page](https://clawhub.ai/devinchen2014/skills/socialdatax-x-twitter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Text or Markdown summaries of X/Twitter search, post, discussion, and creator data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only research results; no account actions.]

## Skill Version(s):

0.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
