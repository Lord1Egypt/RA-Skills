## Description:

Provides Weibo research for trending topics, posts, comments and replies, engagement, and creator profiles and posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to retrieve and review Weibo trends, post details, comments and replies, engagement, and creator information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions run an unpinned CLI package with npx, so package changes between uses can change the code executed.

Mitigation: Review package changes and use a vetted, pinned release where supported; update deliberately.

Risk: Search terms or identifiers used for data requests may be sent to SocialDataX.

Mitigation: Avoid sending sensitive terms or identifiers and confirm SocialDataX is appropriate for the data being requested.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Weibo data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on SocialDataX responses and may be partial when pagination or API errors occur.]

## Skill Version(s):

0.1.24 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
